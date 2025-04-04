from src.orders.models import PosOrderItem
from time import sleep


def run():
    while True:
        item = PosOrderItem.objects.get(number="item-1-04042025-01-2839")
        print(f"item_total: {item.item_total}")
        sleep(3)
