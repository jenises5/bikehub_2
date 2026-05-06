from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from database import database
from dependencies import get_current_user, require_admin
from services.notification_service import create_notification, notify_admin  # ✅ ADDED
import os
import shutil
import uuid

router = APIRouter(prefix="/payment", tags=["Payment"])

UPLOAD_DIR = "uploads/payments"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image(file: UploadFile):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only {ALLOWED_EXTENSIONS} are allowed.",
        )
    return ext


@router.post("/upload-screenshot/{order_id}")
async def upload_screenshot(
    order_id: int, file: UploadFile = File(...), user=Depends(get_current_user)
):
    # Validate file type
    ext = validate_image(file)

    # Check order belongs to user
    order = await database.fetch_one(
        "SELECT id, payment_status, payment_method FROM orders WHERE id = :id AND user_id = :user_id",
        {"id": order_id, "user_id": user["id"]},
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # COD orders don't need screenshots
    if order["payment_method"] == "cod":
        raise HTTPException(
            status_code=400, detail="COD orders don't require payment screenshots"
        )

    # Already paid
    if order["payment_status"] == "paid":
        raise HTTPException(status_code=400, detail="Order is already paid")

    # Already has a pending screenshot — prevent spam
    if order["payment_status"] == "pending_verification":
        raise HTTPException(
            status_code=400,
            detail="Screenshot already uploaded and pending verification. Please wait for admin to review.",
        )

    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="File too large. Maximum size is 5MB."
        )

    # Save file
    filename = f"order_{order_id}_{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(filepath, "wb") as buffer:
        buffer.write(contents)

    # Update order
    await database.execute(
        """
        UPDATE orders SET screenshot_path = :path,
        payment_status = 'pending_verification' WHERE id = :id
        """,
        {"path": filename, "id": order_id},
    )

    # ✅ ADDED — Notify admin that screenshot was uploaded
    await notify_admin(
        f"Payment screenshot uploaded for Order #{order_id} by {user['name']}. Please verify.",
        "payment_uploaded",
    )

    # ✅ ADDED — Notify customer their screenshot was received
    await create_notification(
        user["id"],
        f"Your payment screenshot for Order #{order_id} has been uploaded. Waiting for admin verification.",
        "payment_uploaded",
    )

    return {
        "message": "Screenshot uploaded successfully! Admin will verify your payment shortly.",
        "file": filename,
    }


@router.get("/qr/{method}")
async def get_qr_code(method: str):
    if method not in ["gcash", "maya"]:
        raise HTTPException(status_code=400, detail="Method must be gcash or maya")

    settings = await database.fetch_one("SELECT * FROM shop_settings WHERE id = 1")
    if not settings:
        raise HTTPException(status_code=404, detail="Shop settings not found")

    qr_path = (
        settings["gcash_qr_path"] if method == "gcash" else settings["maya_qr_path"]
    )
    if not qr_path:
        raise HTTPException(status_code=404, detail=f"No {method} QR code uploaded yet")

    return {"method": method, "qr_filename": qr_path}
