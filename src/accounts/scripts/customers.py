from src.accounts.admin.admin_customer import INITIAL_DATA
from src.accounts.models import Customer, User


def initial_data():
    for index, cus in enumerate(INITIAL_DATA):
        customer = Customer.objects.filter(email=cus['email']).first()
        if not customer:
            user = User.objects.get(email='root@root.com')
            customer = Customer(**cus)
            customer.user = user
            customer.save(force_insert=True)
        else:
            customer.email = cus['email']
            customer.code = cus['code']
            customer.is_supplier = cus['is_supplier']
            customer.is_customer = cus['is_customer']
            customer.save(force_update=True)


def run():
    initial_data()
