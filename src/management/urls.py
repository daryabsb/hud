
from django.urls import path
from src.management import views


app_name = 'mgt'

urlpatterns = [
    path('', views.mgt_home, name='mgt-home'),
    path('products/', views.mgt_products, name='products'),
    path('products/<slug:slug>/', views.mgt_products, name='filter-products'),
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

# MODALS URLS
urlpatterns += [
    path('modal-add-group/', views.modal_add_group, name='modal-add-group'),
    path('modal-add-user/', views.modal_add_user, name='modal-add-user'),
    path('modal-add-product/', views.modal_add_product, name='modal-add-product'),
    path('modal-update-product/<int:product_id>/',
         views.modal_add_product, name='modal-update-product'),
    path('modal-add-product-group/', views.modal_add_product_group,
         name='modal-add-product-group'),
    path('modal-update-product-group/', views.modal_update_product_group,
         name='modal-update-product-group'),
    path('modal-delete-product-group/', views.modal_delete_product_group,
         name='modal-delete-product-group'),
]

# HTMX URLS
urlpatterns += [
    path('update-product-group/<slug:slug>/', views.update_product_group,
         name='update-product-group'),
    path('add-product-group/', views.add_product_group,
         name='add-product-group'),

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
    # path('filter-products/<slug:slug>/', mgt_products, name='filter-products'),
]
