from django.conf import settings 
from django.core.mail import EmailMessage 
from django.template import Context 
from django.template.loader import render_to_string 


def send_upload_email(email, message):
    email_subject = 'Upload file'
    email_body = message

    email = EmailMessage(
        email_subject, email_body, settings.DEFAULT_FROM_EMAIL,
        [email], [],
        headers={'Reply-To': email}
    )
    return email.send(fail_silently=False)
