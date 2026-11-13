NOTIFICATION_TYPES = {
    # points notifications
    "POINTS_GAINED": "Points received",
    "POINTS_LOST": "Points deducted",
    "SPONSOR_POINT_CHANGE": "Sponsor point changes",
    "ADMIN_POINT_CHANGE": "Admin point changes",

    # driver-sponsor relationship notifications
    "DRIVER_SPONSOR_ADDED": "Driver connected to a sponsor",
    "DRIVER_SPONSOR_REMOVED": "Driver disconnected from a sponsor",
    "SPONSOR_DRIVER_ADDED": "New driver connected to my company",
    "SPONSOR_DRIVER_REMOVED": "Driver removed from my company",

    # application notifications
    "SPONSOR_NEW_APPLICATION": "New driver applications",
    "ADMIN_NEW_APPLICATION": "New driver applications for admins",
    "APPLICATION_ACCEPTED": "Application accepted",
    "APPLICATION_REJECTED": "Application rejected",
    "ADMIN_APPLICATION_ACCEPTED": "Driver application acceptance alerts",
    "ADMIN_DRIVER_REMOVED": "Driver removal alerts",

    # profile notifications
    "PROFILE_UPDATED": "Profile information updated",

    # order notification types
    "DRIVER_CART_ADDED": "Item added to cart",
    "DRIVER_CART_REMOVED": "Item removed from cart",
    "DRIVER_ORDER_PLACED": "Order placed",
    "DRIVER_ORDER_CANCELED": "Order canceled",
    "DRIVER_ORDER_COMPLETED": "Order completed",

    "SPONSOR_ITEM_ADDED": "Item added to catalog",
    "SPONSOR_ITEM_REMOVED": "Item removed from catalog",
    "SPONSOR_ORDER_PLACED": "New driver order",
    "SPONSOR_ORDER_CANCELED": "Driver canceled order",

    "ADMIN_ORDER_PLACED": "New driver order",
    "ADMIN_ORDER_CANCELED": "Driver canceled order",
}

ROLE_NOTIFICATION_TYPES = {
    "Driver": [
        "POINTS_GAINED",
        "POINTS_LOST",
        "APPLICATION_ACCEPTED",
        "APPLICATION_REJECTED",
        "DRIVER_SPONSOR_ADDED",
        "DRIVER_SPONSOR_REMOVED",
        "PROFILE_UPDATED",
        "DRIVER_CART_ADDED",
        "DRIVER_CART_REMOVED",
        "DRIVER_ORDER_PLACED",
        "DRIVER_ORDER_CANCELED",
        "DRIVER_ORDER_COMPLETED"
    ],
    "Sponsor": [
        "SPONSOR_NEW_APPLICATION",
        "SPONSOR_DRIVER_ADDED",
        "SPONSOR_DRIVER_REMOVED",
        "SPONSOR_POINT_CHANGE",
        "PROFILE_UPDATED",
        "SPONSOR_ITEM_ADDED",
        "SPONSOR_ITEM_REMOVED",
        "SPONSOR_ORDER_PLACED",
        "SPONSOR_ORDER_CANCELED"
    ],
    "Admin": [
        "ADMIN_NEW_APPLICATION",
        "ADMIN_APPLICATION_ACCEPTED",
        "ADMIN_DRIVER_REMOVED",
        "ADMIN_POINT_CHANGE",
        "PROFILE_UPDATED",
        "ADMIN_ORDER_PLACED",
        "ADMIN_ORDER_CANCELED"
    ]
}

def create_notification (
    cursor,
    user_id,
    notification_type,
    title,
    message,
    pointchange_id=None,
    application_id=None
):
    """
    Creates notifications for users.
    If the user disabled the notif type,
    no notification is created.
    If the user have not saved preferences,
    default is enabled.
    """

    # check if user had disabled notification type
    cursor.execute("""
        SELECT IS_ENABLED
        FROM NOTIFICATIONSETTINGS
        WHERE USER_ID = %s
            AND NOTIFICATION_TYPE = %s
    """, (user_id, notification_type))

    setting = cursor.fetchone()

    # no saved setting means all notifications are enabled
    if setting and not setting["IS_ENABLED"]:
        return

    # create the notification
    cursor.execute("""
        INSERT INTO NOTIFICATIONS (
            USER_ID,
            NOTIFICATION_TYPE,
            TITLE,
            MESSAGE,
            POINTCHANGE_ID,
            APPLICATION_ID
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        notification_type,
        title,
        message,
        pointchange_id,
        application_id
    ))