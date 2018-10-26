from django.core.mail import send_mail
from celery.decorators import task


@task(name='send_email_to_users')
def send_email(subject, message, from_email, to_email):
    send_mail(subject, message, from_email, to_email)
