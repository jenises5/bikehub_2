from fastapi import APIRouter, Depends
from database import database
from dependencies import require_admin

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def get_dashboard(admin=Depends(require_admin)):
    # Revenue today
    revenue_today = await database.fetch_one("""
        SELECT COALESCE(SUM(total_amount), 0) as total
        FROM orders
        WHERE payment_status = 'paid'
        AND DATE(created_at) = CURRENT_DATE
        """)

    # Revenue this week
    revenue_week = await database.fetch_one("""
        SELECT COALESCE(SUM(total_amount), 0) as total
        FROM orders
        WHERE payment_status = 'paid'
        AND created_at >= DATE_TRUNC('week', CURRENT_DATE)
        """)

    # Revenue this month
    revenue_month = await database.fetch_one("""
        SELECT COALESCE(SUM(total_amount), 0) as total
        FROM orders
        WHERE payment_status = 'paid'
        AND created_at >= DATE_TRUNC('month', CURRENT_DATE)
        """)

    # Total revenue all time
    revenue_total = await database.fetch_one("""
        SELECT COALESCE(SUM(total_amount), 0) as total
        FROM orders
        WHERE payment_status = 'paid'
        """)

    # Order counts by status
    order_counts = await database.fetch_all("""
        SELECT status, COUNT(*) as count
        FROM orders
        GROUP BY status
        ORDER BY count DESC
        """)

    # Pending payment verifications
    pending_verification = await database.fetch_one("""
        SELECT COUNT(*) as count FROM orders
        WHERE payment_status = 'pending_verification'
        """)

    # Total customers
    total_customers = await database.fetch_one("""
        SELECT COUNT(*) as count FROM users
        WHERE role = 'customer'
        """)

    # Low stock products
    low_stock = await database.fetch_all("""
        SELECT p.name, p.stock_quantity, p.low_stock_threshold,
               b.name as brand_name
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.stock_quantity <= p.low_stock_threshold
        AND p.is_active = TRUE
        ORDER BY p.stock_quantity ASC
        """)

    return {
        "revenue": {
            "today": float(revenue_today["total"]),
            "this_week": float(revenue_week["total"]),
            "this_month": float(revenue_month["total"]),
            "all_time": float(revenue_total["total"]),
        },
        "orders": {
            "by_status": [dict(row) for row in order_counts],
            "pending_verification": pending_verification["count"],
        },
        "customers": {"total": total_customers["count"]},
        "low_stock_products": [dict(row) for row in low_stock],
    }


@router.get("/top-products")
async def get_top_products(admin=Depends(require_admin)):
    # Top by quantity sold
    by_quantity = await database.fetch_all("""
        SELECT p.name, b.name as brand_name,
               SUM(oi.quantity) as total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        LEFT JOIN brands b ON p.brand_id = b.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.payment_status = 'paid'
        GROUP BY p.id, p.name, b.name
        ORDER BY total_sold DESC
        LIMIT 10
        """)

    # Top by revenue generated
    by_revenue = await database.fetch_all("""
        SELECT p.name, b.name as brand_name,
               SUM(oi.quantity * oi.price_at_purchase) as total_revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        LEFT JOIN brands b ON p.brand_id = b.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.payment_status = 'paid'
        GROUP BY p.id, p.name, b.name
        ORDER BY total_revenue DESC
        LIMIT 10
        """)

    return {
        "top_by_quantity": [dict(row) for row in by_quantity],
        "top_by_revenue": [dict(row) for row in by_revenue],
    }


@router.get("/revenue-chart")
async def get_revenue_chart(admin=Depends(require_admin)):
    # Last 30 days revenue per day
    daily = await database.fetch_all("""
        SELECT DATE(created_at) as date,
               COALESCE(SUM(total_amount), 0) as revenue,
               COUNT(*) as order_count
        FROM orders
        WHERE payment_status = 'paid'
        AND created_at >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY DATE(created_at)
        ORDER BY date ASC
        """)

    return {
        "daily_revenue": [
            {
                "date": str(row["date"]),
                "revenue": float(row["revenue"]),
                "order_count": row["order_count"],
            }
            for row in daily
        ]
    }
