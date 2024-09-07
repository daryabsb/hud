
from django.urls import path
from src.management import views


app_name = 'mgt'

urlpatterns = [
    path('', views.mgt_home, name='mgt-home'),
    path('stocks/', views.mgt_stocks, name='stocks'),
    path('users/', views.mgt_users, name='users'),
    path('update-permissions/', views.mgt_update_permissions,
            name='update-permissions'),
    path('update-group-permissions/', views.mgt_update_group_permissions,
            name='update-group-permissions'),

    path('add-product/', views.add_product,
            name='add-product'),
    path('update-product/<int:product_id>/', views.add_product,
            name='update-product'),
]

# PRODUCTS RELATED URLS

urlpatterns += [
    path('products/', views.mgt_products, name='products'),
    path('products/<slug:slug>/', views.mgt_products, name='filter-products'),
    path('price-tags/', views.mgt_price_tags, name='price-tags'),
    path('price-tags/<slug:slug>', views.mgt_price_tags, name='filter-price-tags'),
    path('invoice-template/', views.mgt_invoice_template_view,
            name='invoice-template'),
    path('mgt-price-tags-control/', views.mgt_price_tags_control,
            name='mgt-price-tags-control'),

    path(
        "products-datatable-data/",
        views.product_datatable_view,
        name="products-datatable-data",
    ),
    #     path('products-list/', views.ProductListView.as_view(),
    #          name='products-list'),

]

# DOCUMENTS RELATED URLS

urlpatterns += [
    path('documents/', views.mgt_documents, name='documents'),
    path('add-document/', views.add_document, name='add-document'),
    path('documents/test/', views.mgt_documents_example, name='documents-example'),
    path('documents-datatable-data/', views.documents_datatable_view,
        name='documents-datatable-data'),
]

# DOCUMENTS RELATED URLS
urlpatterns += [
    path('document-items-datatable/',
        views.document_items_datatable_view, name='document-items-datatable'),
    path('documents/test/', views.mgt_documents_example, name='documents-example'),
]


# MODALS URLS
urlpatterns += [
    path('modal-add-group/', views.modal_add_group, name='modal-add-group'),
    path('modal-add-user/', views.modal_add_user, name='modal-add-user'),
    path('modal-add-product/', views.modal_add_product, name='modal-add-product'),
    path('modal-select-document-type/', views.modal_select_document_type,
            name='modal-select-document-type'),
    path('modal-add-document/', views.modal_add_document,
            name='modal-add-document'),
    path('modal-update-product/',
            views.modal_add_product, name='modal-update-product'),
    path('modal-add-product-group/', views.modal_add_product_group,
            name='modal-add-product-group'),
    path('modal-update-product-group/', views.modal_update_product_group,
            name='modal-update-product-group'),
    path('modal-delete-product/', views.modal_delete_product,
            name='modal-delete-product'),
    path('modal-delete-product-group/', views.modal_delete_product_group,
            name='modal-delete-product-group'),
    path('modal-select-product-fields/', views.select_product_fields_to_export,
            name='modal-select-product-fields'),
    path('add-new-document-tab/', views.add_new_document_tab, name='add-new-document-tab')
]

# HTMX URLS
urlpatterns += [
    path('update-product-group/<slug:slug>/', views.update_product_group,
            name='update-product-group'),
    path('add-product-group/', views.add_product_group,
            name='add-product-group'),

    path('delete-product/', views.delete_product,
            name='delete-product'),
    path('delete-product-group/', views.delete_product_group,
            name='delete-product-group'),
    path('show-customer-form/', views.show_customer_form,
            name='show-customer-form'),
    path('append-product-tax-form/', views.append_product_tax_form,
            name='append-product-tax-form'),
    path('generate-barcode/', views.generate_barcode_for_product,
            name='generate-barcode'),
    path('add-to-producttax-formset/', views.add_to_product_tax_formset,
            name='add-to-producttax-formset'),
    path('delete-product-tax/', views.delete_product_tax,
            name='delete-product-tax'),
    # path('filter-products/<slug:slug>/', mgt_products, name='filter-products'),

    path('price-tag-preview/', views.mgt_price_tags_preview,
            name="price-tag-preview"),
    path('price-tag-set-default/', views.mgt_price_tags_set_default,
            name="price-tag-set-default"),
    path('price-tag-print-selected/', views.mgt_price_tags_print_selected,
            name="price-tag-print-selected"),
    path('export-products-to-csv/', views.mgt_export_products_to_csv,
            name="export-products-to-csv"),
    path('export-products-to-excel/', views.mgt_export_products_to_excel,
            name="export-products-to-excel"),

    path('filter-document-type/', views.filter_document_type,
            name="filter-document-type"),

        
]


# API VIEWS
urlpatterns += [
    path('api/documents/', views.DocumentListView.as_view(),
            name='document-list-api'),
    path('api/documents/data', views.get_document_data,
            name='document-data'),
    # other routes
    path(
        "item_datatable/",
        views.ItemListView.as_view(),
        name="item_datatable",
    ),
]
