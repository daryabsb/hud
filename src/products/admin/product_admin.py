from django.contrib import admin
from src.accounts.models import User
from src.products.models import Product, ProductGroup, Currency
from django.utils.translation import gettext as _

INITIAL_DATA = [
    {"id": 1, "name": "Organic Bananas", "parent_group": 1, "price": 1200, "rank": 1},
    {"id": 2, "name": "WholeMilk", "parent_group": 1, "price": 3500, "rank": 2},
    {"id": 3, "name": "ChickenBreast", "parent_group": 1, "price": 5000, "rank": 3},
    {"id": 4, "name": "SourdoughBread", "parent_group": 1, "price": 4000, "rank": 4},
    {"id": 5, "name": "TomatoSoup", "parent_group": 1, "price": 1500, "rank": 5},
    {"id": 6, "name": "iPhone11ProMax",
        "parent_group": 2, "price": 1050000, "rank": 6},
    {"id": 7, "name": "DELLLavender13in",
        "parent_group": 2, "price": 740000, "rank": 7},
    {"id": 8, "name": "SamsungRefrigerator",
        "parent_group": 2, "price": 1200000, "rank": 8},
    {"id": 9, "name": "SonyWH-1000XM4", "parent_group": 2, "price": 350000, "rank": 9},
    {"id": 10, "name": "CanonEOSR5", "parent_group": 2, "price": 3900000, "rank": 10},
    {"id": 11, "name": "ModernSofa", "parent_group": 3, "price": 850000, "rank": 11},
    {"id": 12, "name": "EgyptianCottonSheets",
        "parent_group": 3, "price": 120000, "rank": 12},
    {"id": 13, "name": "NonstickCookwareSet",
        "parent_group": 3, "price": 200000, "rank": 13},
    {"id": 14, "name": "AbstractWallArt",
        "parent_group": 3, "price": 80000, "rank": 14},
    {"id": 15, "name": "DysonVacuumCleaner",
        "parent_group": 3, "price": 300000, "rank": 15},
    {"id": 16, "name": "GoldNecklace", "parent_group": 4, "price": 450000, "rank": 16},
    {"id": 17, "name": "LeatherHandbag",
        "parent_group": 4, "price": 250000, "rank": 17},
    {"id": 18, "name": "RolexSubmariner",
        "parent_group": 4, "price": 8000000, "rank": 18},
    {"id": 19, "name": "Ray-BanAviator",
        "parent_group": 4, "price": 150000, "rank": 19},
    {"id": 20, "name": "CashmereScarf",
        "parent_group": 4, "price": 200000, "rank": 20},
    {"id": 21, "name": "BelgianChocolates",
        "parent_group": 5, "price": 25000, "rank": 21},
    {"id": 22, "name": "PotatoChips", "parent_group": 5, "price": 3000, "rank": 22},
    {"id": 23, "name": "GummyBears", "parent_group": 5, "price": 5000, "rank": 23},
    {"id": 24, "name": "TruffleOil", "parent_group": 5, "price": 30000, "rank": 24},
    {"id": 25, "name": "HolidayGiftBasket",
        "parent_group": 5, "price": 60000, "rank": 25}
]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_group', 'user', 'created')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, product in enumerate(INITIAL_DATA):
            pdct = Product.objects.filter(slug=(product['id'])).first()
            if not pdct:
                user = User.objects.get(email='root@root.com')
                parent_id = product.pop('parent_group')
                currency = Currency.objects.filter(code='IQD').first()
                parent_group = ProductGroup.objects.get(id=parent_id)
                pdct = Product(**product)

                pdct.user = user
                pdct.currency = currency
                pdct.parent_group = parent_group
                pdct.save(force_insert=True)
                print("p slug is ", pdct.slug)
                pdct.image = f"initial/{pdct.slug}.jpg"
                pdct.save(force_update=True)
            else:
                pdct.name = product['name']
                pdct.save(force_update=True)
