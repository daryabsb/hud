from django.db import IntegrityError
from src.products.models import Barcode, Product
from src.accounts.models import User
from django.core.exceptions import ObjectDoesNotExist


def run():
    user = User.objects.first()
    products = Product.objects.all()

    b_products = set()

    for b in Barcode.objects.all():
        b_products.add(b.product.id)
    
    print(b_products)

    for product in products:
        print(product.id not in b_products)
        if product.id in b_products:
            print('Barcode already exist for ', product.name)
            continue
        else:
            barcode = Barcode(user=user, product=product)
            barcode.save()
            b_products.add(barcode.product.id)
            print(barcode.product.name)
        

    # for product in products:
    #     try:
    #         product.barcode
    #     except ObjectDoesNotExist:
    #         created = False
    #         while not created:
    #             try:
    #                 barcode = Barcode.objects.create(
    #                     user=user, product=product)
    #                 created = True
    #                 print("Barcode value is:", barcode.value)
    #             except IntegrityError:
    #                 # Handle duplicate EAN-13 value and retry
    #                 print("Duplicate EAN-13 value generated, retrying...")

