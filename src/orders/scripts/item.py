from src.orders.models import PosOrderItem, PosOrder
from time import sleep
from src.orders.api.serializers import PosOrderItemSerializer, PosOrderSerializer


def run():
    # items = PosOrderItem.objects.filter(order__number='sales-06122024-3773')
    orders = PosOrder.objects.all()
    data = PosOrderSerializer(orders, many=True).data
    # for order in data:
    print(data[0])

