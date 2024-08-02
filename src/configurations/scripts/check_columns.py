from src.core.utils import get_fields, get_columns


def run():
    print(get_fields('products'))
    print(get_columns('products'))


[
    'id', 'name', 'slug', 'code', 'description', 'plu', 'measurement_unit', 'price', 'is_tax_inclusive_price',
    'is_price_change_allowed', 'is_service', 'is_using_default_quantity', 'cost', 'margin', 'image', 'color',
    'is_enabled', 'age_restriction', 'last_purchase_price', 'rank', 'created', 'updated']

[
    {'name': 'id', 'title': 'Id'},
    {'name': 'name', 'title': 'Name'},
    {'name': 'slug', 'title': 'Slug'},
    {'name': 'code', 'title': 'Code'},
    {'name': 'description', 'title': 'Description'},
    {'name': 'plu', 'title': 'Plu'},
    {'name': 'measurement_unit', 'title': 'Measurement Unit'},
    {'name': 'price', 'title': 'Price'},
    {'name': 'is_tax_inclusive_price', 'title': 'Is Tax Inclusive Price'},
    {'name': 'is_price_change_allowed', 'title': 'Is Price Change Allowed'},
    {'name': 'is_service', 'title': 'Is Service'},
    {'name': 'is_using_default_quantity', 'title': 'Is Using Default Quantity'},
    {'name': 'cost', 'title': 'Cost'},
    {'name': 'margin', 'title': 'Margin'},
    {'name': 'image', 'title': 'Image'},
    {'name': 'color', 'title': 'Color'},
    {'name': 'is_enabled', 'title': 'Is Enabled'},
    {'name': 'age_restriction', 'title': 'Age Restriction'},
    {'name': 'last_purchase_price', 'title': 'Last Purchase Price'},
    {'name': 'rank', 'title': 'Rank'},
    {'name': 'created', 'title': 'Created'},
    {'name': 'updated', 'title': 'Updated'}
]
