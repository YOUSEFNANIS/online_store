from online_store.celery import celery
from django.core.mail import send_mail, BadHeaderError

@celery.task
def message_seller(id, email):
    
    body = f'order number #{id} has been completed'
    send_mail(subject='', message=body, from_email='nanisyousof@gmail.com',recipient_list=[email])
