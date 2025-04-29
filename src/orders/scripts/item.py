from src.orders.models import PosOrderItem, PosOrder, get_orders
from time import sleep
from src.orders.api.serializers import PosOrderItemSerializer, PosOrderSerializer
from src.core.utils import recursive_to_dict


def run():
    # items = PosOrderItem.objects.filter(order__number='sales-06122024-3773')
    # orders = PosOrder.objects.all()
    # data = PosOrderSerializer(orders, many=True).data
    # for order in data:
    print(get_orders(refresh=True)[1])
