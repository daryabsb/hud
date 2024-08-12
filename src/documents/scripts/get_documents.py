from src.documents.models import Document, DocumentType, DocumentItem
from src.accounts.models import User, Customer, Warehouse
from src.pos.models import CashRegister
from src.orders.models import PosOrder
import random, decimal
from django.forms import model_to_dict

types = DocumentType.objects.all()
user = User.objects.first()
cash_register = CashRegister.objects.first()
warehouse = Warehouse.objects.first()
order = PosOrder.objects.first()
customers = Customer.objects.all()


def create_number():
    return random.randint(5000,150000)

def create_total():
    return random.uniform(3500.00,1500000.00)

def random_bool():
    return random.choice((True,False))

def random_qs(qs):
    return random.choice(qs)

def random_set(n):
    return random.sample(range(1, 25), n)

def random_one_digit():
    return random.randint(1,10)
    


def run():
    # create_documents()
    document_item = DocumentItem.objects.first()
    print(model_to_dict(document_item))

    # documents = Document.objects.first()
    # print(model_to_dict(documents))
    # print(decimal.Decimal(create_number()))
    # print(random_type())
    # print(str(create_number()))


def create_documents():
    for doc in range(50):
        document = {
            'number': str(create_number()), 
            'user': user, 
            'customer': random_qs(customers), 
            'cash_register': cash_register, 
            'order': order, 
            'document_type': random_qs(types), 
            'warehouse': warehouse, 
            'reference_document_number': str(create_number()), 
            'internal_note': '', 
            'note': '', 'discount': 0, 
            'discount_type': 0, 
            'discount_apply_rule': 0, 
            'paid_status': random_bool(), 
            'total': decimal.Decimal(create_number()), 
            'is_clocked_out': random_bool()
            }
        # print(document)
        Document.objects.create(**document)

def create_document_items():
    item = {
        'id': 1, 
        'user': 1, 
        'document': 2, 
        'product': 1, 
        'quantity': 1, 
        'expected_quantity': 1, 
        'price_before_tax': 2500.0, 
        'price': 2500.0, 
        'discount': 0.0, 
        'discount_type': 0.0, 
        'product_cost': 2300.0, 
        'price_before_tax_after_discount': 2500.0, 
        'price_after_discount': 2500.0, 
        'total': 2500.0, 
        'total_after_document_discount': 2500.0, 
        'discount_apply_rule': 0, 
        'returned': False
        }