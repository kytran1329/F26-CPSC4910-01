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