
from django.urls import path
from src.management.views import (
    mgt_home, mgt_products, mgt_stocks, mgt_users,
    mgt_update_permissions, mgt_update_group_permissions,
    modal_add_group
)


app_name = 'mgt'

urlpatterns = [
    path('', mgt_home, name='mgt-home'),
    path('products/', mgt_products, name='products'),
    path('stocks/', mgt_stocks, name='stocks'),
    path('users/', mgt_users, name='users'),
    path('update-permissions/', mgt_update_permissions, name='update-permissions'),
    path('update-group-permissions/', mgt_update_group_permissions,
         name='update-group-permissions'),
]

# MODALS URLS
urlpatterns += [
    path('modal-add-group/', modal_add_group, name='modal-add-group'),

] 