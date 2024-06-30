
from django.urls import path
from src.management.views import (
    mgt_home, mgt_products, mgt_stocks, mgt_users,
    mgt_update_permissions, mgt_update_group_permissions,
    modal_add_group, modal_add_user, modal_add_product, modal_add_product_group,
    modal_delete_product_group, modal_update_product_group,
    add_product_group, update_product_group, delete_product_group,
    add_product,

)


app_name = 'mgt'

urlpatterns = [
     path('', mgt_home, name='mgt-home'),
     path('products/', mgt_products, name='products'),
     path('products/<slug:slug>/', mgt_products, name='filter-products'),
     path('stocks/', mgt_stocks, name='stocks'),
     path('users/', mgt_users, name='users'),
     path('update-permissions/', mgt_update_permissions, name='update-permissions'),
     path('update-group-permissions/', mgt_update_group_permissions,
          name='update-group-permissions'),

     path('add-product/', add_product,
          name='add-product'),
]

# MODALS URLS
urlpatterns += [
     path('modal-add-group/', modal_add_group, name='modal-add-group'),
     path('modal-add-user/', modal_add_user, name='modal-add-user'),
     path('modal-add-product/', modal_add_product, name='modal-add-product'),
     path('modal-add-product-group/', modal_add_product_group,
          name='modal-add-product-group'),
     path('modal-update-product-group/', modal_update_product_group,
          name='modal-update-product-group'),
     path('modal-delete-product-group/', modal_delete_product_group,
          name='modal-delete-product-group'),
]

# HTMX URLS
urlpatterns += [
     path('update-product-group/<slug:slug>/', update_product_group,
          name='update-product-group'),
     path('add-product-group/', add_product_group,
          name='add-product-group'),

     path('delete-product-group/', delete_product_group,
          name='delete-product-group'),

     # path('filter-products/<slug:slug>/', mgt_products, name='filter-products'),
]
