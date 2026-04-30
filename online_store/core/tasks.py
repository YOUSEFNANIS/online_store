from online_store.celery import celery
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
@celery.task
def message_seller(id, email):
    
    body = f'order number #{id} has been completed'
    send_mail(subject='', message=body, from_email='nanisyousof@gmail.com',recipient_list=[email])

@celery.task
def send_order_message(order_number, user_email):
    subject = f"Your Receipt for Order #{order_number}"
    message = f"Thank you for shopping at JR Shop! Your order #{order_number} is confirmed."
    html_message = f"<h1>Order Confirmed</h1><p>Thank you for your order <strong>#{order_number}</strong>.</p>"
    send_mail(
                subject=subject,
                message=message,
                from_email='nanisyousof@gmail.com',
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
    return Response({"message": "Receipt sent successfully!"}, status=status.HTTP_200_OK)