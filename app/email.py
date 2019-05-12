from app import mail
from flask import current_app
from flask_mail import Message
from threading import Thread


def send_async_email(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subjet, text_body, html_body, sender, recipient):
    message = Message(subjet, sender=sender, recipients=recipient)
    message.body = text_body
    message.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), message)).start()