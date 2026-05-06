from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from database import database
from dependencies import require_admin
import os
import shutil
import uuid

router = APIRouter(prefix="/settings", tags=["Settings"])

QR_DIR = "uploads/qr"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def validate_image(file: UploadFile):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only {ALLOWED_EXTENSIONS} are allowed.",
        )
    return ext


class ShopSettingsUpdate(BaseModel):
    shop_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    hours: Optional[str] = None
    delivery_fee: Optional[float] = None
    is_pickup_enabled: Optional[bool] = None
    is_cod_enabled: Optional[bool] = None
    is_gcash_enabled: Optional[bool] = None
    is_maya_enabled: Optional[bool] = None


@router.get("/")
async def get_settings():
    settings = await database.fetch_one("SELECT * FROM shop_settings WHERE id = 1")
    if not settings:
        raise HTTPException(status_code=404, detail="Shop settings not found")
    return dict(settings)


@router.put("/")
async def update_settings(body: ShopSettingsUpdate, admin=Depends(require_admin)):
    updates = {k: v for k, v in body.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join([f"{k} = :{k}" for k in updates])
    await database.execute(
        f"UPDATE shop_settings SET {set_clause} WHERE id = 1", updates
    )
    return {"message": "Shop settings updated!"}


@router.post("/upload-qr/{method}")
async def upload_qr(
    method: str, file: UploadFile = File(...), admin=Depends(require_admin)
):
    if method not in ["gcash", "maya"]:
        raise HTTPException(status_code=400, detail="Method must be gcash or maya")

    ext = validate_image(file)

    # Check file size
    contents = await file.read()
    if len(contents) > 2 * 1024 * 1024:  # 2MB max for QR codes
        raise HTTPException(
            status_code=400, detail="File too large. Maximum size is 2MB."
        )

    filename = f"{method}_qr_{uuid.uuid4()}.{ext}"
    filepath = os.path.join(QR_DIR, filename)
    os.makedirs(QR_DIR, exist_ok=True)

    with open(filepath, "wb") as buffer:
        buffer.write(contents)

    column = "gcash_qr_path" if method == "gcash" else "maya_qr_path"
    await database.execute(
        f"UPDATE shop_settings SET {column} = :filename WHERE id = 1",
        {"filename": filename},
    )

    return {
        "message": f"{method.upper()} QR code uploaded successfully!",
        "filename": filename,
    }
