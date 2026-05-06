from fastapi import APIRouter, Depends
from database import database
from dependencies import get_current_user, require_admin

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/")
async def get_my_notifications(
    limit: int = 20, offset: int = 0, user=Depends(get_current_user)
):
    rows = await database.fetch_all(
        """
        SELECT * FROM notifications
        WHERE user_id = :user_id
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :offset
        """,
        {"user_id": user["id"], "limit": limit, "offset": offset},
    )
    return [dict(row) for row in rows]


@router.get("/unread-count")
async def get_unread_count(user=Depends(get_current_user)):
    result = await database.fetch_one(
        """
        SELECT COUNT(*) as count FROM notifications
        WHERE user_id = :user_id AND is_read = FALSE
        """,
        {"user_id": user["id"]},
    )
    return {"unread_count": result["count"]}


@router.put("/mark-read/{notification_id}")
async def mark_as_read(notification_id: int, user=Depends(get_current_user)):
    await database.execute(
        """
        UPDATE notifications SET is_read = TRUE
        WHERE id = :id AND user_id = :user_id
        """,
        {"id": notification_id, "user_id": user["id"]},
    )
    return {"message": "Notification marked as read!"}


@router.put("/mark-all-read")
async def mark_all_read(user=Depends(get_current_user)):
    await database.execute(
        """
        UPDATE notifications SET is_read = TRUE
        WHERE user_id = :user_id AND is_read = FALSE
        """,
        {"user_id": user["id"]},
    )
    return {"message": "All notifications marked as read!"}


@router.delete("/{notification_id}")
async def delete_notification(notification_id: int, user=Depends(get_current_user)):
    await database.execute(
        """
        DELETE FROM notifications
        WHERE id = :id AND user_id = :user_id
        """,
        {"id": notification_id, "user_id": user["id"]},
    )
    return {"message": "Notification deleted!"}
