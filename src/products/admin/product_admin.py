from django.contrib import admin
from src.accounts.models import User
from src.products.models import Product, ProductGroup, Currency
from django.utils.translation import gettext as _

INITIAL_DATA = [
    {"id": 1, "name": "Organic Bananas", "parent_group": 2,
        "price": 1200, "rank": 1, "measurement_unit": "KG"},
    {"id": 2, "name": "WholeMilk", "parent_group": 2,
        "price": 3500, "rank": 2, "measurement_unit": "packs"},
    {"id": 3, "name": "ChickenBreast", "parent_group": 2,
        "price": 5000, "rank": 3, "measurement_unit": "KG"},
    {"id": 4, "name": "SourdoughBread", "parent_group": 2,
        "price": 4000, "rank": 4, "measurement_unit": "pcs"},
    {"id": 5, "name": "TomatoSoup", "parent_group": 2,
        "price": 1500, "rank": 5, "measurement_unit": "pcs"},
    {"id": 6, "name": "iPhone11ProMax",
        "parent_group": 3, "price": 1050000, "rank": 6, "measurement_unit": "pcs"},
    {"id": 7, "name": "DELLLavender13in",
        "parent_group": 3, "price": 740000, "rank": 7, "measurement_unit": "pcs"},
    {"id": 8, "name": "SamsungRefrigerator",
        "parent_group": 3, "price": 1200000, "rank": 8, "measurement_unit": "pcs"},
    {"id": 9, "name": "SonyWH-1000XM4", "parent_group": 3,
        "price": 350000, "rank": 9, "measurement_unit": "pcs"},
    {"id": 10, "name": "CanonEOSR5", "parent_group": 3,
        "price": 3900000, "rank": 10, "measurement_unit": "pcs"},
    {"id": 11, "name": "ModernSofa", "parent_group": 4,
        "price": 850000, "rank": 11, "measurement_unit": "pcs"},
    {"id": 12, "name": "EgyptianCottonSheets",
        "parent_group": 4, "price": 120000, "rank": 12, "measurement_unit": "pcs"},
    {"id": 13, "name": "NonstickCookwareSet",
        "parent_group": 4, "price": 200000, "rank": 13, "measurement_unit": "pcs"},
    {"id": 14, "name": "AbstractWallArt",
        "parent_group": 4, "price": 80000, "rank": 14, "measurement_unit": "pcs"},
    {"id": 15, "name": "DysonVacuumCleaner",
        "parent_group": 4, "price": 300000, "rank": 15, "measurement_unit": "pcs"},
    {"id": 16, "name": "GoldNecklace", "parent_group": 5,
        "price": 450000, "rank": 16, "measurement_unit": "pcs"},
    {"id": 17, "name": "LeatherHandbag",
        "parent_group": 5, "price": 250000, "rank": 17, "measurement_unit": "pcs"},
    {"id": 18, "name": "RolexSubmariner",
        "parent_group": 5, "price": 8000000, "rank": 18, "measurement_unit": "pcs"},
    {"id": 19, "name": "Ray-BanAviator",
        "parent_group": 5, "price": 150000, "rank": 19, "measurement_unit": "pcs"},
    {"id": 20, "name": "CashmereScarf",
        "parent_group": 5, "price": 200000, "rank": 20, "measurement_unit": "pcs"},
    {"id": 21, "name": "BelgianChocolates",
        "parent_group": 6, "price": 25000, "rank": 21, "measurement_unit": "pcs"},
    {"id": 22, "name": "PotatoChips", "parent_group": 6,
        "price": 3000, "rank": 22, "measurement_unit": "pcs"},
    {"id": 23, "name": "GummyBears", "parent_group": 6,
        "price": 5000, "rank": 23, "measurement_unit": "pcs"},
    {"id": 24, "name": "TruffleOil", "parent_group": 6,
        "price": 30000, "rank": 24, "measurement_unit": "pcs"},
    {"id": 25, "name": "HolidayGiftBasket",
        "parent_group": 6, "price": 60000, "rank": 25, "measurement_unit": "pcs"}
]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_group', 'slug', 'user', 'created')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, product in enumerate(INITIAL_DATA):
            pdct = Product.objects.filter(id=(product['id'])).first()
            currency = Currency.objects.filter(code='IQD').first()
            parent_id = product.pop('parent_group')
            parent_group = ProductGroup.objects.get(id=parent_id)
            if not pdct:
                user = User.objects.get(email='root@root.com')
                pdct = Product(**product)

                pdct.user = user
                pdct.currency = currency
                pdct.parent_group = parent_group
                pdct.save(force_insert=True)
                print("p slug is ", pdct.slug)
                pdct.image = f"initial/{pdct.slug}.jpg"
                pdct.save(force_update=True)
            else:
                pdct.parent_group = parent_group
                pdct.measurement_unit = product['measurement_unit']
                pdct.save(force_update=True)
