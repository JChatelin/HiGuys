from app.email import send_mail
from flask import current_app, render_template


def send_reset_password_email(user):
    token = user.get_reset_password_token()
    send_mail('[HiGuys] Reset Your Password',
              sender=current_app.config['ADMINS'][0],
              recipient=[user.email],
              text_body=render_template('auth/email/reset_password.txt', user=user, token=token),
              html_body=render_template('auth/email/reset_password.html', user=user, token=token))
