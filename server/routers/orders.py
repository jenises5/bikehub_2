from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from database import database
from dependencies import get_current_user, require_admin
from services.notification_service import create_notification, notify_admin  # ✅ ADDED

router = APIRouter(prefix="/orders", tags=["Orders"])


class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CheckoutRequest(BaseModel):
    fulfillment_type: str
    payment_method: str
    delivery_address: Optional[str] = None


# --- CART ROUTES ---
@router.post("/cart/add")
async def add_to_cart(body: CartItemAdd, user=Depends(get_current_user)):
    product = await database.fetch_one(
        "SELECT id, stock_quantity FROM products WHERE id = :id AND is_active = TRUE",
        {"id": body.product_id},
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product["stock_quantity"] < body.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    existing = await database.fetch_one(
        "SELECT id, quantity FROM cart_items WHERE user_id = :user_id AND product_id = :product_id",
        {"user_id": user["id"], "product_id": body.product_id},
    )
    if existing:
        await database.execute(
            "UPDATE cart_items SET quantity = quantity + :qty WHERE id = :id",
            {"qty": body.quantity, "id": existing["id"]},
        )
    else:
        await database.execute(
            "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (:user_id, :product_id, :quantity)",
            {
                "user_id": user["id"],
                "product_id": body.product_id,
                "quantity": body.quantity,
            },
        )
    return {"message": "Added to cart!"}


@router.get("/cart")
async def get_cart(user=Depends(get_current_user)):
    rows = await database.fetch_all(
        """
        SELECT ci.id, ci.quantity, p.id as product_id, p.name, p.price, p.image_url, p.stock_quantity
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.user_id = :user_id
        """,
        {"user_id": user["id"]},
    )
    items = [dict(row) for row in rows]
    total = float(sum(item["price"] * item["quantity"] for item in items))
    return {"items": items, "total": total}


@router.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: int, user=Depends(get_current_user)):
    await database.execute(
        "DELETE FROM cart_items WHERE user_id = :user_id AND product_id = :product_id",
        {"user_id": user["id"], "product_id": product_id},
    )
    return {"message": "Item removed from cart!"}


@router.delete("/cart/clear")
async def clear_cart(user=Depends(get_current_user)):
    await database.execute(
        "DELETE FROM cart_items WHERE user_id = :user_id", {"user_id": user["id"]}
    )
    return {"message": "Cart cleared!"}


# --- ORDER ROUTES ---
@router.post("/checkout")
async def checkout(body: CheckoutRequest, user=Depends(get_current_user)):
    valid_methods = ["cod", "gcash", "maya"]
    if body.payment_method not in valid_methods:
        raise HTTPException(
            status_code=400, detail=f"Payment method must be one of: {valid_methods}"
        )

    if body.fulfillment_type not in ["pickup", "delivery"]:
        raise HTTPException(
            status_code=400, detail="Fulfillment type must be pickup or delivery"
        )

    if body.fulfillment_type == "delivery" and not body.delivery_address:
        raise HTTPException(
            status_code=400, detail="Delivery address is required for delivery orders"
        )

    items = await database.fetch_all(
        """
        SELECT ci.quantity, p.id as product_id, p.price, p.stock_quantity, p.name
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.user_id = :user_id
        """,
        {"user_id": user["id"]},
    )
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in items:
        if item["stock_quantity"] < item["quantity"]:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {item['name']}. Only {item['stock_quantity']} left.",
            )

    settings = await database.fetch_one(
        "SELECT delivery_fee FROM shop_settings WHERE id = 1"
    )
    delivery_fee = (
        float(settings["delivery_fee"]) if body.fulfillment_type == "delivery" else 0.0
    )
    subtotal = float(sum(item["price"] * item["quantity"] for item in items))
    total = subtotal + delivery_fee

    if body.payment_method == "cod":
        initial_payment_status = "cod_pending"
        initial_status = "confirmed"
    else:
        initial_payment_status = "unpaid"
        initial_status = "pending"

    order_id = await database.execute(
        """
        INSERT INTO orders (user_id, total_amount, status, fulfillment_type, payment_method,
        delivery_address, delivery_fee, payment_status)
        VALUES (:user_id, :total_amount, :status, :fulfillment_type, :payment_method,
        :delivery_address, :delivery_fee, :payment_status)
        RETURNING id
        """,
        {
            "user_id": user["id"],
            "total_amount": total,
            "status": initial_status,
            "fulfillment_type": body.fulfillment_type,
            "payment_method": body.payment_method,
            "delivery_address": body.delivery_address,
            "delivery_fee": delivery_fee,
            "payment_status": initial_payment_status,
        },
    )

    for item in items:
        await database.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
            VALUES (:order_id, :product_id, :quantity, :price)
            """,
            {
                "order_id": order_id,
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price": item["price"],
            },
        )
        await database.execute(
            "UPDATE products SET stock_quantity = stock_quantity - :qty WHERE id = :id",
            {"qty": item["quantity"], "id": item["product_id"]},
        )

    await database.execute(
        "DELETE FROM cart_items WHERE user_id = :user_id", {"user_id": user["id"]}
    )

    if body.payment_method == "cod":
        next_step = "Your order is confirmed! Pay cash upon pickup/delivery."
    else:
        next_step = f"Please upload your {body.payment_method.upper()} payment screenshot to confirm your order."

    # ✅ ADDED — Notify admin of new order
    await notify_admin(
        f"New order #{order_id} from {user['name']} — ₱{total:,.2f} via {body.payment_method.upper()}",
        "new_order",
    )

    # ✅ ADDED — Notify customer their order was placed
    await create_notification(
        user["id"],
        f"Your order #{order_id} has been placed! Total: ₱{total:,.2f}. {next_step}",
        "new_order",
    )

    return {
        "message": "Order placed successfully!",
        "order_id": order_id,
        "total": total,
        "delivery_fee": delivery_fee,
        "payment_method": body.payment_method,
        "next_step": next_step,
    }


@router.get("/my-orders")
async def get_my_orders(user=Depends(get_current_user)):
    rows = await database.fetch_all(
        "SELECT * FROM orders WHERE user_id = :user_id ORDER BY created_at DESC",
        {"user_id": user["id"]},
    )
    return [dict(row) for row in rows]


@router.get("/my-orders/{order_id}")
async def get_order_detail(order_id: int, user=Depends(get_current_user)):
    order = await database.fetch_one(
        "SELECT * FROM orders WHERE id = :id AND user_id = :user_id",
        {"id": order_id, "user_id": user["id"]},
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = await database.fetch_all(
        """
        SELECT oi.quantity, oi.price_at_purchase, p.name, p.image_url
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = :order_id
        """,
        {"order_id": order_id},
    )
    return {"order": dict(order), "items": [dict(i) for i in items]}


# --- ADMIN ROUTES ---
@router.get("/admin/all")
async def get_all_orders(admin=Depends(require_admin)):
    rows = await database.fetch_all("""
        SELECT o.*, u.name as customer_name, u.email as customer_email
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
        """)
    return [dict(row) for row in rows]


@router.put("/admin/{order_id}/status")
async def update_order_status(order_id: int, status: str, admin=Depends(require_admin)):
    valid_statuses = [
        "pending",
        "confirmed",
        "processing",
        "ready",
        "delivered",
        "cancelled",
    ]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400, detail=f"Status must be one of: {valid_statuses}"
        )

    existing = await database.fetch_one(
        "SELECT id FROM orders WHERE id = :id", {"id": order_id}
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")

    await database.execute(
        "UPDATE orders SET status = :status WHERE id = :id",
        {"status": status, "id": order_id},
    )

    # ✅ ADDED — Notify customer their order status changed
    order = await database.fetch_one(
        "SELECT user_id FROM orders WHERE id = :id", {"id": order_id}
    )
    await create_notification(
        order["user_id"],
        f"Your order #{order_id} status has been updated to: {status.upper()}",
        "new_order",
    )

    return {"message": f"Order status updated to {status}!"}


@router.put("/admin/{order_id}/verify-payment")
async def verify_payment(order_id: int, admin=Depends(require_admin)):
    order = await database.fetch_one(
        "SELECT id, payment_status, user_id FROM orders WHERE id = :id",
        {"id": order_id},
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order["payment_status"] == "paid":
        raise HTTPException(status_code=400, detail="Payment already verified")

    await database.execute(
        "UPDATE orders SET payment_status = 'paid', status = 'confirmed' WHERE id = :id",
        {"id": order_id},
    )

    # ✅ ADDED — Notify customer payment was verified
    await create_notification(
        order["user_id"],
        f"Your payment for Order #{order_id} has been verified! Your order is now confirmed.",
        "payment_verified",
    )

    return {"message": "Payment verified! Order confirmed."}


@router.put("/admin/{order_id}/reject-payment")
async def reject_payment(order_id: int, reason: str, admin=Depends(require_admin)):
    order = await database.fetch_one(
        "SELECT id, payment_status, user_id FROM orders WHERE id = :id",
        {"id": order_id},
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await database.execute(
        """
        UPDATE orders SET payment_status = 'rejected',
        rejected_reason = :reason WHERE id = :id
        """,
        {"reason": reason, "id": order_id},
    )

    # ✅ ADDED — Notify customer payment was rejected
    await create_notification(
        order["user_id"],
        f"Your payment for Order #{order_id} was rejected. Reason: {reason}. Please upload a new screenshot.",
        "payment_rejected",
    )

    return {"message": "Payment rejected. Customer will be notified."}
