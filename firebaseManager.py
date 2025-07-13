import firebase_admin
from firebase_admin import credentials, messaging

class FirebaseManager:
    def __init__(self, cred_path=None):
        if not firebase_admin._apps:
            if cred_path:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                # Initialize with default credentials (if available)
                firebase_admin.initialize_app()

    def send_to_token(self, token, title, body, channel_id=None):
        android_config = None
        if channel_id:
            android_config = messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    channel_id=channel_id
                )
            )
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            android=android_config
        )
        try:
            response = messaging.send(message)
            print("Successfully sent message:", response)
            return response
        except Exception as e:
            print("Error sending message:", e)
            return None
