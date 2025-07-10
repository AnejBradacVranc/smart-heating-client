import firebase_admin
from firebase_admin import messaging


default_app = firebase_admin.initialize_app()


message = messaging.Message(
    notification=messaging.Notification(
        title='Hello!',
        body='This is a test notification sent via Firebase Cloud Messaging.',
    ),
    token='your-device-fcm-token-here'  # Replace with a valid FCM device token
)

response = messaging.send(message)
print('Successfully sent message:', response)
