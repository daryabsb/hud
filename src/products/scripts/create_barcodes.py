from django.db import IntegrityError
from src.products.models import Barcode, Product
from src.accounts.models import User
from django.core.exceptions import ObjectDoesNotExist


def run():
    user = User.objects.first()
    products = Product.objects.all()

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
    for barcode in Barcode.objects.all():
        # barcode.value = ''
        barcode.save(force_update=True)
