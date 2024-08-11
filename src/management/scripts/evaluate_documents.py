from src.products.models import Product

filter_dict = {
    "name__icontains": "TomatoSoup"
}


def run():
    products = Product.objects.all()

    products = products.filter(**filter_dict)

    for product in products:
        print(product.name)
