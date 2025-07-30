from django.urls import path, include
from src.pos2 import views
from src.pos2.views.modal_views import GenericOrderModalView

app_name = "pos2"

urlpatterns = [
    path('', views.pos_home, name='pos-home'),
    path('<str:number>/', views.pos_order, name='pos-order'),
]

urlpatterns += [
    path('add/order-item/', views.AddOrderItemView.as_view(), name="add-item"),
]

urlpatterns += [
    path('update/active-order/status/<str:number>/',
         views.StatusUpdateView.as_view(), name='update-order-status'),
    path('update/active-order/note/<str:number>/',
         views.CommentUpdateView.as_view(), name='update-order-note'),
    path('update/active-order/internal-note/<str:number>/',
         views.InternalNoteUpdateView.as_view(), name='update-order-internal-note'),
    #     path('update/active-order/discount/<str:number>/',
    #          views.DiscountUpdateView.as_view(), name='update-order-discount'),
    # Generic update endpoint that can handle any field
    #     path('update/active-order/<str:number>/',
    #          views.GenericOrderUpdateView.as_view(), name='update-order-generic'),
    # Modal view for the generic order update form
    path('modal/update-order/<str:number>/',
         GenericOrderModalView.as_view(), name='modal-update-order-generic'),
]

urlpatterns += [
    path('modal/pos-modal-search/',
         views.pos_search_modal, name='pos-modal-search'),
]
