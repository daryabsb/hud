
# const.py
import inspect
import random

ORDER_STATUS = (
    (1, 'Unfulfilled'),
    (2, 'Ready for pickup'),
    (3, 'Ready for delivery'),
    (4, 'Cancelled'),
    (5, 'Fulfilled'),
)


def get_view_name():
    return inspect.stack()[2].function  # corrected level for decorator


def get_template_for_view():
    return MY_TEMPLATES.get(get_view_name())


MY_TEMPLATES = {
    'add_new_order': 'cotton/orders/order.html',
    'delete_active_order': 'cotton/orders/order.html',
}

'''
1. create an order with:
    required: user, document_type, is_active=False
    defaults: customer, warehouse=default_warehouse

2. asign customer if exist, else move on
3. add items to the order, minimum 1
4. create a document with document_item
5. create payment:
    - if payment amount == order_total => move on
    - else: leave the order (partially paid), close the document, 
        create new payment for the same document if happened
    - documents can have multiple payments until done for cases like:
        * pay the rest later
        * pay in split
        * pay with different payment_types such as cash, card or others
    - if more or less paid, the customer balance will reflect the differences
'''


def create_fake_order(is_active=False):
    from src.orders.models import PosOrder, PosOrderItem, PosOrderStatus
    from src.accounts.models import Customer, User
    from src.products.models import Product
    # Get the first order status (created)
    status = PosOrderStatus.objects.get(ordinal=8)
    user = User.objects.first()

    # Create a new order
    order = PosOrder.objects.create(
        is_enabled=True,
        is_active=is_active,
        status=status,
        user=user
    )

    # Replace with a random customer
    random_customer = Customer.objects.order_by('?').first()
    if random_customer:
        order.customer = random_customer
        order.save()

    # Select random bundle products
    products = Product.objects.filter(is_bundle=True)
    if products.exists():
        for _ in range(random.randint(1, 5)):  # Add 1 to 5 products
            product = random.choice(products)
            quantity = random.randint(1, 10)

            # Create PosOrderItem
            PosOrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

    return order
