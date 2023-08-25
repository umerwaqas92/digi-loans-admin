import firebase_admin
from firebase_admin import credentials,initialize_app, messaging

cred = credentials.Certificate("app/digiloans-510a0-firebase-adminsdk-w3ci2-a6b225625f.json")
firebase_admin.initialize_app(cred)

def send_notification_to_user(topic_name, notification_title, notification_body):
    print("Sending notification to user", topic_name, notification_title, notification_body)
    # Initialize Firebase app with your service account key

    
    # Create a message to send
    message = messaging.Message(
        topic=topic_name,

        notification=messaging.Notification(
            title=notification_title,
            body=notification_body
        )
    )
    
    # Send the message
    response = messaging.send(message)
    return response


# send_notification_to_user("user_roman01gmailcom","tesy","test")