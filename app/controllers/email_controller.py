from app import mail
from app.models.dbmodels import Manager
from flask_mail import Message
from flask import render_template, current_app
from threading import Thread


class EmailController:

    @staticmethod
    def send_async_email(app: current_app, msg: Message):
        with app.app_context():
            mail.send(msg)

    @staticmethod
    def send_email(subject: str, sender: str, recipients: list, text_body: str, html_body: str):
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body

        Thread(target=EmailController.send_async_email, args=(current_app._get_current_object(), msg)).start()

    @staticmethod
    def send_password_reset_email(user: Manager):
        token = user.get_reset_password_token()

        EmailController.send_email(
            subject='Reset Your Password',
            sender=current_app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('email/reset_password.txt',
                                      user=user, token=token),
            html_body=render_template('email/reset_password.html',
                                      user=user, token=token)
        )
