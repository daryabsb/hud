from src.orders.models import PosOrder
from celery import shared_task

@shared_task
def create_order_every_5_minutes():
    print('something good!')