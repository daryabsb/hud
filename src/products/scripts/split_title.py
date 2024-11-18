import re
from src.products.models import Product


def run():
    products = Product.objects.all()

    for product in products:
        title = product.name
        result = re.findall(r'[A-Z][a-z]*', title)
        product_name = ' '.join(result)
        product.name = product_name
        product.save()

        # print(product.name)
print('Done!')
