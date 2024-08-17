from django.contrib import admin
from src.documents.models import (
    Document, DocumentCategory, DocumentItem, DocumentType
)
from src.accounts.models import User
from django.utils.translation import gettext as _


document_category_initial_data = [
    {'id': 1, 'name': 'Sales', 'user_id': 1},
    {'id': 2, 'name': 'Expenses', 'user_id': 1},
    {'id': 3, 'name': 'Inventory', 'user_id': 1},
    {'id': 4, 'name': 'Loss and Damages', 'user_id': 1},
]
document_type_initial_data = [
    {'id': 1, 'name': 'Purchase', 'code': 100, 'stock_direction': 1, 'print_template':
        'Purchase', 'price_type': 2, 'category_id': 2, 'user_id': 1},
    {'id': 2, 'name': 'Sales', 'code': 200,	'stock_direction': 2, 'print_template':
        'Invoice', 'price_type': 1, 'category_id': 1, 'user_id': 1},
    {'id': 3, 'name': 'Inventory Count', 'code': 300, 'stock_direction': 1, 'print_template':
        'InventoryCount', 'price_type': 0, 'category_id': 3, 'user_id': 1},
    {'id': 4, 'name': 'Refund', 'code': 220, 'stock_direction': 1, 'print_template':
        'Refund', 'price_type': 1, 'category_id': 1, 'user_id': 1},
    {'id': 5, 'name': 'Stock Return', 'code': 120,	'stock_direction': 2, 'print_template':
     'StockReturn', 'price_type': 2, 'category_id': 1, 'user_id': 1},
    {'id': 6, 'name': 'Loss And Damage', 'code': 400, 'stock_direction': 2,
        'print_template': 'LossAndDamage', 'price_type': 0, 'category_id': 4, 'user_id': 1},
    {'id': 7, 'name': 'Proforma', 'code': 230, 'stock_direction': 0,
        'print_template': 'Proforma', 'price_type': 1, 'category_id': 1, 'user_id': 1},
]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'discount', 'discount_type',
                    'total', 'paid_status', 'date')
    ordering = ('-date', )
    list_filter = ('date', 'paid_status', )

    def product_name(self, obj):
        from django.forms import model_to_dict
        doc_item = obj.document_items.all().first()
        if doc_item:
            item_name = obj.document_items.first().product.name
        #     if item:
        #         item_name = item.plan.subscription.name
        #         return item_name if item_name else ""
            return item_name
        return ''
    product_name.short_description = 'Document Item'


@admin.register(DocumentItem)
class DocumentItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'total', 'returned', 'created')
    ordering = ('-created', )
    # list_filter = ('user', 'product__plan__subscription')

    def total(self, obj):
        return obj.total_after_document_discount
    #     return obj.name"
    total.short_description = 'Total'


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created')
    ordering = ('id', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, category in enumerate(document_category_initial_data):
            user = User.objects.get(id=category['user_id'])
            if not user:
                user = User.objects.first()
            cat = DocumentCategory.objects.filter(id=category['id']).first()
            if not cat:
                cat_user = category.pop('user_id')
                cat = DocumentCategory(**category)
                cat.user = user
                cat.save(force_insert=True)
            else:
                cat.name = category['name']
                cat.save(force_update=True)

    def get_queryset(self, request):
        qs = super(DocumentCategoryAdmin, self).get_queryset(request)
        return qs


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'category', 'user', 'created')
    ordering = ('id', )
    list_filter = ('name', 'category', )

    @staticmethod
    def initial_data():
        for index, type in enumerate(document_type_initial_data):
            doc_type = DocumentType.objects.filter(code=type['code']).first()
            if not doc_type:
                user = User.objects.get(id=type['user_id'])
                category = DocumentCategory.objects.get(id=type['category_id'])
                if not user:
                    user = User.objects.first()
                if not category:
                    continue
                doc_type_user = type.pop('user_id')
                doc_type_category = type.pop('category_id')
                doc_type = DocumentType(**type)
                doc_type.user = user
                doc_type.category = category
                doc_type.save(force_insert=True)
            else:
                doc_type.code = type['code']
                doc_type.save(force_update=True)

    def get_queryset(self, request):
        qs = super(DocumentTypeAdmin, self).get_queryset(request)
        return qs
