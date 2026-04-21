import random

from django.core.mail import send_mail
from django.conf import settings


def random_otp():
  return random.randint(1000,9999)

def send_otp_email(email, otp):
    subject = 'Your OTP for Verification'
    message = f'''
    <h1>Your OTP for Verification</h1>
    <p>Your OTP is: {otp}</p>
    <p>This OTP will expire in 10 minutes</p>
    <p>Thank you</p>
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    fail_silently=False
    send_mail(subject, message, email_from, recipient_list,fail_silently=fail_silently)

