from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

def send_register_email_otp(email, otp):
    subject = 'Account verification OTP from BookTrade'
    html_message = render_to_string('authentication/new_user_otp_template.html', {'otp': otp})
    plain_message = strip_tags(html_message)
    from_email = '"BookTrade App" <app.booktrade@gmail.com>'
    to_email = email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

def send_forget_password_email_otp(email, otp):
    subject = 'Password reset otp for BookTrade'
    html_message = render_to_string('authentication/forget_password_otp_template.html', {'otp': otp})
    plain_message = strip_tags(html_message)
    from_email = '"BookTrade App" <app.booktrade@gmail.com>'
    to_email = email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)