from src.core.utils import get_fields, get_columns
from src.documents.models import DocumentItem
from src.configurations.models import AppTableColumn


def run():
    searchable_fields = [
        {"id": 1, "app": "products", "name": "id", "title": "Id",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },
        {"id": 2, "app": "products", "name": "code", "title": "Code",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },
        {"id": 3, "app": "products", "name": "image", "title": "Image",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 4, "app": "products", "name": "name", "title": "Name",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": True, },
        {"id": 5, "app": "products", "name": "slug", "title": "Slug",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 6, "app": "products", "name": "barcode", "title": "Barcode",
         "is_enabled": True, "is_related": True, "related_value": "barcode__value", "searchable": True, },
        {"id": 7, "app": "products", "name": "parent_group", "title": "Parent Group",
         "is_enabled": True, "is_related": True, "related_value": "parent_group__name", "searchable": True, },
        {"id": 8, "app": "products", "name": "price", "title": "Price",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 9, "app": "products", "name": "cost", "title": "Cost",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 10, "app": "products", "name": "last_purchase_price", "title": "Last Purchase Price",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 11, "app": "products", "name": "margin", "title": "Margin",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 12, "app": "products", "name": "measurement_unit", "title": "Measurement Unit",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 13, "app": "products", "name": "currency", "title": "Currency",
         "is_enabled": True, "is_related": True, "related_value": "currency__name", "searchable": False, },
        {"id": 14, "app": "products", "name": "rank", "title": "Rank",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 15, "app": "products", "name": "plu", "title": "Plu",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 16, "app": "products", "name": "user", "title": "User",
         "is_enabled": True, "is_related": True, "related_value": "user__name", "searchable": False, },
        {"id": 17, "app": "products", "name": "color", "title": "Color",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 18, "app": "products", "name": "description", "title": "Description",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },

        {"id": 19, "app": "products", "name": "is_tax_inclusive_price", "title": "Is Tax Inclusive Price",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 20, "app": "products", "name": "is_price_change_allowed",
         "title": "Is Price Change Allowed", "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 21, "app": "products", "name": "is_service", "title": "Is Service",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 22, "app": "products", "name": "is_using_default_quantity",
         "title": "Is Using Default Quantity", "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 23, "app": "products", "name": "is_product", "title": "Is Product",
         "is_enabled": False, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 24, "app": "products", "name": "is_enabled", "title": "Is Enabled",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 25, "app": "products", "name": "age_restriction", "title": "Age Restriction",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 26, "app": "products", "name": "created", "title": "Created",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
        {"id": 27, "app": "products", "name": "updated", "title": "Updated",
         "is_enabled": True, "is_related": False, "related_value": "", "searchable": False, },
    ]

    flat_list = [field['name']
                 for field in searchable_fields if field['searchable']]

    for field in AppTableColumn.objects.filter(app__name="products"):
        if field.name not in flat_list:
            field.searchable = False
            field.save()
            print(field.name)

    # print(get_fields('products'))
    # print(get_columns('products'))
