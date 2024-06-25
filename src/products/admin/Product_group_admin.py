from django.contrib import admin
from src.accounts.models import User
from src.products.models import ProductGroup

INITIAL_DATA = [
    {"id": 1, "name": "Products", "slug": "products", "rank": 1},
    {"id": 2, "name": "Grocery", "slug": "grocery", "rank": 2},
    {"id": 3, "name": "Electronics", "slug": "electronics", "rank": 8},
    {"id": 4, "name": "Home", "slug": "home", "rank": 14},
    {"id": 5, "name": "Accessories", "slug": "accessories", "rank": 20},
    {"id": 6, "name": "Goodies", "slug": "goodies", "rank": 26},
]


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'user', 'created')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, group in enumerate(INITIAL_DATA):
            grp = ProductGroup.objects.filter(slug=(group['slug'])).first()
            if not grp:
                user = User.objects.get(email='root@root.com')
                grp = ProductGroup(**group)
                grp.user = user
                grp.image = f"initial/{group['slug']}.jpg"
                grp.save(force_insert=True)
            else:
                grp.slug = group['slug']
                grp.save(force_update=True)

    def get_queryset(self, request):
        qs = super(ProductGroupAdmin, self).get_queryset(request)
        # qs = qs.exclude(code__in=[
        #  const.CODE_ACTUAL_BREAK, const.CODE_ACTUAL_WORKED, const.CODE_DAY_OFF, const.CODE_WEEKEND,
        #  const.CODE_HOLIDAY])
        return qs

    def has_add_permission(self, request):
        return True


initial_data_with_parents = [
    # Grocery
    {"id": 6, "name": "Fresh Produce", "parent": 2,
        "slug": "fresh_produce", "rank": 2},
    {"id": 7, "name": "Dairy Products", "parent": 2,
        "slug": "dairy_products", "rank": 3},
    {"id": 8, "name": "Meat & Seafood", "parent": 2,
        "slug": "meat_seafood", "rank": 4},
    {"id": 9, "name": "Bakery Items", "parent": 2,
        "slug": "bakery_items", "rank": 5},
    {"id": 10, "name": "Canned Goods", "parent": 2,
        "slug": "canned_goods", "rank": 6},

    # Electronics
    {"id": 11, "name": "Mobile Phones", "parent": 3,
        "slug": "mobile_phones", "rank": 8},
    {"id": 12, "name": "Laptops", "parent": 3, "slug": "laptops", "rank": 9},
    {"id": 13, "name": "Home Appliances", "parent": 3,
        "slug": "home_appliances", "rank": 10},
    {"id": 14, "name": "Audio & Video", "parent": 3,
        "slug": "audio_video", "rank": 11},
    {"id": 15, "name": "Cameras & Photography",
        "parent": 3, "slug": "cameras_photography", "rank": 12},

    # Home
    {"id": 16, "name": "Furniture", "parent": 4, "slug": "furniture", "rank": 14},
    {"id": 17, "name": "Bedding & Bath", "parent": 4,
        "slug": "bedding_bath", "rank": 15},
    {"id": 18, "name": "Kitchenware", "parent": 4,
        "slug": "kitchenware", "rank": 16},
    {"id": 19, "name": "Home Decor", "parent": 4, "slug": "home_decor", "rank": 17},
    {"id": 20, "name": "Cleaning Supplies",
        "parent": 4, "slug": "cleaning_supplies", "rank": 18},

    # Accessories
    {"id": 21, "name": "Jewelry", "parent": 5, "slug": "jewelry", "rank": 20},
    {"id": 22, "name": "Handbags", "parent": 5, "slug": "handbags", "rank": 21},
    {"id": 23, "name": "Watches", "parent": 5, "slug": "watches", "rank": 22},
    {"id": 24, "name": "Sunglasses", "parent": 5, "slug": "sunglasses", "rank": 23},
    {"id": 25, "name": "Scarves", "parent": 5, "slug": "scarves", "rank": 24},

    # Goodies
    {"id": 26, "name": "Chocolates", "parent": 6, "slug": "chocolates", "rank": 26},
    {"id": 27, "name": "Snacks", "parent": 6, "slug": "snacks", "rank": 27},
    {"id": 28, "name": "Candies", "parent": 6, "slug": "candies", "rank": 28},
    {"id": 29, "name": "Gourmet Foods", "parent": 6,
        "slug": "gourmet_foods", "rank": 29},
    {"id": 30, "name": "Gift Baskets", "parent": 6,
        "slug": "gift_baskets", "rank": 30},
]


more_initial_data = {
    "grocery_list": [
        {"id": 1, "name": "Organic Bananas",
            "category": "Fresh Produce", "price": 1.2},
        {"id": 2, "name": "Whole Milk", "category": "Dairy Products", "price": 3.5},
        {"id": 3, "name": "Chicken Breast",
            "category": "Meat & Seafood", "price": 5.0},
        {"id": 4, "name": "Sourdough Bread",
            "category": "Bakery Items", "price": 4.0},
        {"id": 5, "name": "Tomato Soup", "category": "Canned Goods", "price": 1.5}
    ],
    "electronics_list": [
        {"id": 1, "name": "iPhone 11 Max Pro",
         "category": "Mobile Phones", "price": 1050},
        {"id": 2, "name": "DELL Lavender 13in",
            "category": "Laptops", "price": 740},
        {"id": 3, "name": "Samsung Refrigerator",
         "category": "Home Appliances", "price": 1200},
        {"id": 4, "name": "Sony WH-1000XM4",
            "category": "Audio & Video", "price": 350},
        {"id": 5, "name": "Canon EOS R5",
         "category": "Cameras & Photography", "price": 3900}
    ],
    "home_list": [
        {"id": 1, "name": "Modern Sofa", "category": "Furniture", "price": 850},
        {"id": 2, "name": "Egyptian Cotton Sheets",
         "category": "Bedding & Bath", "price": 120},
        {"id": 3, "name": "Nonstick Cookware Set",
         "category": "Kitchenware", "price": 200},
        {"id": 4, "name": "Abstract Wall Art",
            "category": "Home Decor", "price": 80},
        {"id": 5, "name": "Dyson Vacuum Cleaner",
         "category": "Cleaning Supplies", "price": 300}
    ],
    "accessories_list": [
        {"id": 1, "name": "Gold Necklace", "category": "Jewelry", "price": 450},
        {"id": 2, "name": "Leather Handbag", "category": "Handbags", "price": 250},
        {"id": 3, "name": "Rolex Submariner", "category": "Watches", "price": 8000},
        {"id": 4, "name": "Ray-Ban Aviator", "category": "Sunglasses", "price": 150},
        {"id": 5, "name": "Cashmere Scarf", "category": "Scarves", "price": 200}
    ],
    "goodies_list": [
        {"id": 1, "name": "Belgian Chocolates",
            "category": "Chocolates", "price": 25},
        {"id": 2, "name": "Potato Chips", "category": "Snacks", "price": 3},
        {"id": 3, "name": "Gummy Bears", "category": "Candies", "price": 5},
        {"id": 4, "name": "Truffle Oil", "category": "Gourmet Foods", "price": 30},
        {"id": 5, "name": "Holiday Gift Basket",
         "category": "Gift Baskets", "price": 60}
    ]

}

# Sure, here are five subcategory names for each of the given categories:

# ### Grocery
# 1. Fresh Produce
# 2. Dairy Products
# 3. Meat & Seafood
# 4. Bakery Items
# 5. Canned Goods

# ### Electronics
# 1. Mobile Phones
# 2. Laptops
# 3. Home Appliances
# 4. Audio & Video
# 5. Cameras & Photography

# ### Home
# 1. Furniture
# 2. Bedding & Bath
# 3. Kitchenware
# 4. Home Decor
# 5. Cleaning Supplies

# ### Accessories
# 1. Jewelry
# 2. Handbags
# 3. Watches
# 4. Sunglasses
# 5. Scarves

# ### Goodies
# 1. Chocolates
# 2. Snacks
# 3. Candies
# 4. Gourmet Foods
# 5. Gift Baskets
