import plyer

def create_notification(title, subtitle):
    plyer.notification.notify(
        app_name="Aletheia",
        title=title,
        message=subtitle,
        app_icon="../Assets/icon.ico", 
        timeout=3,     
    )