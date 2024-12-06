from src.documents.models import Document, DocumentType, DocumentItem
from src.accounts.models import User, Customer, Warehouse
from src.pos.models import CashRegister
from src.orders.models import PosOrder
from src.products.models import Product
import random
import decimal
from django.forms import model_to_dict

documents = Document.objects.all()
types = DocumentType.objects.all()
user = User.objects.first()
cash_register = CashRegister.objects.first()
warehouse = Warehouse.objects.first()
order = PosOrder.objects.first()
customers = Customer.objects.all()


def run():
    # create_documents()
    create_document_items()
    # print(str(create_number()))
    # product = Product.objects.first()
    # print("filtered_product = ", product.name)
    # documents = Document.objects.filter(
    #     document_items__product=product
    # ).distinct()
    # print(documents.count(), "documents found")
    # checked_documents = 0
    # for document in documents:
    #     for item in document.document_items.all():
    #         if item.product == product:
    #             checked_documents += 1
    # print(checked_documents, "documents checked")
    # print("found_product = ", item.product.name)


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
    from src.core.utils import generate_number
    for document in documents:
        n = random_one_digit()
        products_ids = random_set(n)
        product_name_list = []
        if document.document_items.exists():
            print('document items exists')
        else:
            for id in products_ids:
                product = Product.objects.get(id=id)
                quantity = random_one_digit()
                # total = float(product.price) * float(quantity)

                item = DocumentItem(**{
                    'number': generate_number('item'),
                    'user': user,
                    'document': document,
                    'product': product,
                    'quantity': quantity,
                    'expected_quantity': 1,
                    # 'price_before_tax': product.price,
                    'price': product.price,
                    'discount': 0.0,
                    'discount_type': 0.0,
                    # 'product_cost': float(product.price) * float(0.90),
                    # 'price_before_tax_after_discount': product.price,
                    # 'price_after_discount': product.price,
                    # 'total': total,
                    # 'total_after_document_discount': total,
                    'discount_apply_rule': 0,
                    'returned': random_bool()
                })
                item.save()
                print(
                    f'{item.product.name}: {item.price} X {item.quantity} = {item.price * item.quantity}')


def create_number():
    return random.randint(5000, 150000)


def create_total():
    return random.uniform(3500.00, 1500000.00)


def random_bool():
    return random.choice((True, False))


def random_qs(qs):
    return random.choice(qs)


def random_set(n):
    return random.sample(range(1, 25), n)


def random_one_digit():
    return random.randint(3, 12)
