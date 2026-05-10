from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from database import database
from dependencies import get_current_user, require_admin
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import os
import uuid

router = APIRouter(prefix="/products", tags=["Products"])


# --- SCHEMAS ---
class ProductCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int
    low_stock_threshold: int = 5
    brand_id: Optional[int] = None
    category: str
    riding_style: Optional[str] = None
    frame_size: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    brand_id: Optional[int] = None
    category: Optional[str] = None
    riding_style: Optional[str] = None
    frame_size: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


# --- PUBLIC ROUTES ---
@router.get("/")
async def get_products(
    category: Optional[str] = None,
    brand_id: Optional[int] = None,
    riding_style: Optional[str] = None,
    frame_size: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    query = """
        SELECT p.*, b.name as brand_name, b.tier as brand_tier
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.is_active = TRUE
    """
    params = {}

    if category:
        query += " AND p.category = :category"
        params["category"] = category
    if brand_id:
        query += " AND p.brand_id = :brand_id"
        params["brand_id"] = brand_id
    if riding_style:
        query += " AND p.riding_style = :riding_style"
        params["riding_style"] = riding_style
    if frame_size:
        query += " AND p.frame_size = :frame_size"
        params["frame_size"] = frame_size
    if min_price is not None:
        query += " AND p.price >= :min_price"
        params["min_price"] = min_price
    if max_price is not None:
        query += " AND p.price <= :max_price"
        params["max_price"] = max_price

    query += " ORDER BY p.created_at DESC"
    rows = await database.fetch_all(query, params)
    return [dict(row) for row in rows]


@router.get("/admin/all")
async def get_all_products_admin(admin=Depends(require_admin)):
    rows = await database.fetch_all("""
        SELECT p.*, b.name as brand_name, b.tier as brand_tier
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        ORDER BY p.created_at DESC
        """)
    return [dict(row) for row in rows]


@router.get("/admin/low-stock")
async def get_low_stock(admin=Depends(require_admin)):
    rows = await database.fetch_all("""
        SELECT p.*, b.name as brand_name
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.stock_quantity <= p.low_stock_threshold AND p.is_active = TRUE
        """)
    return [dict(row) for row in rows]


@router.get("/{id}")
async def get_product(id: int):
    row = await database.fetch_one(
        """
        SELECT p.*, b.name as brand_name, b.tier as brand_tier
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.id = :id AND p.is_active = TRUE
        """,
        {"id": id},
    )
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(row)


# --- ADMIN ROUTES ---
@router.post("/")
async def create_product(body: ProductCreate, admin=Depends(require_admin)):
    query = """
        INSERT INTO products
        (name, price, stock_quantity, low_stock_threshold, brand_id,
         category, riding_style, frame_size, description, image_url)
        VALUES
        (:name, :price, :stock_quantity, :low_stock_threshold, :brand_id,
         :category, :riding_style, :frame_size, :description, :image_url)
        RETURNING id
    """
    product_id = await database.execute(query, dict(body))
    return {"message": "Product created!", "id": product_id}


@router.put("/{id}")
async def update_product(id: int, body: ProductUpdate, admin=Depends(require_admin)):
    existing = await database.fetch_one(
        "SELECT id FROM products WHERE id = :id", {"id": id}
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = {k: v for k, v in body.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join([f"{k} = :{k}" for k in updates])
    updates["id"] = id
    await database.execute(f"UPDATE products SET {set_clause} WHERE id = :id", updates)
    return {"message": "Product updated!"}


@router.delete("/{id}")
async def delete_product(id: int, admin=Depends(require_admin)):
    existing = await database.fetch_one(
        "SELECT id FROM products WHERE id = :id", {"id": id}
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    await database.execute(
        "UPDATE products SET is_active = FALSE WHERE id = :id", {"id": id}
    )
    return {"message": "Product deleted!"}


PRODUCT_IMAGE_DIR = "uploads/products"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


@router.post("/{id}/upload-image")
async def upload_product_image(
    id: int, file: UploadFile = File(...), admin=Depends(require_admin)
):
    # Check product exists
    product = await database.fetch_one(
        "SELECT id FROM products WHERE id = :id", {"id": id}
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Validate file type
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only {ALLOWED_EXTENSIONS} are allowed.",
        )

    # Check file size (max 5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max 5MB.")

    # Save file
    os.makedirs(PRODUCT_IMAGE_DIR, exist_ok=True)
    filename = f"product_{id}_{uuid.uuid4()}.{ext}"
    filepath = os.path.join(PRODUCT_IMAGE_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    # Update product image_url
    image_url = f"/uploads/products/{filename}"
    await database.execute(
        "UPDATE products SET image_url = :image_url WHERE id = :id",
        {"image_url": image_url, "id": id},
    )

    return {
        "message": "Product image uploaded!",
        "image_url": image_url,
        "full_url": f"http://localhost:8000{image_url}",
    }
