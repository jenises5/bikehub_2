from database import database


async def create_notification(user_id: int, message: str, type: str):
    """
    Reusable function to create a notification for any user.
    Call this from any router whenever something important happens.

    Types: new_order, payment_uploaded, payment_verified,
           payment_rejected, low_stock
    """
    try:
        await database.execute(
            """
            INSERT INTO notifications (user_id, message, type)
            VALUES (:user_id, :message, :type)
            """,
            {"user_id": user_id, "message": message, "type": type},
        )
    except Exception as e:
        # Never let notification failure break the main flow
        print(f"⚠️ Notification failed: {e}")


async def notify_admin(message: str, type: str):
    """
    Shortcut to notify all admin users at once.
    """
    try:
        admins = await database.fetch_all("SELECT id FROM users WHERE role = 'admin'")
        for admin in admins:
            await create_notification(admin["id"], message, type)
    except Exception as e:
        print(f"⚠️ Admin notification failed: {e}")
