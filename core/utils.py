from django.conf import settings
from django.core.mail import send_mail
import uuid


def send_email_token(email , token):
     try:
          subject = 'Please verify your account below'
          message = f'Click on the link to verify http://127.0.0.1:8000/verify/{token}/'
          email_from = settings.EMAIL_HOST_USER
          recipient_list = [email, ]
          send_mail( subject, message, email_from, recipient_list ) 
          
     except Exception as e:
          return False
     
     return True

def send_forget_password_mail(email, token):
     subject = 'Your forget password link'
     message = f'Click on the link to reset your Password http://127.0.0.1:8000/change-password/{token}/'
     email_from = settings.EMAIL_HOST_USER
     recipient_list = [email, ]
     send_mail( subject, message, email_from, recipient_list )
     
     return True