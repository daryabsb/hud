from django.urls import path, include
from src.pos2 import views

app_name = "pos2"

urlpatterns = [
    path('', views.pos_home, name='pos-home'),
    path('<str:number>/', views.pos_order, name='pos-order'),
]

urlpatterns += [
    path('update/active-order/status/<str:number>/',
         views.StatusUpdateView.as_view(), name='update-order-status'),
    path('update/active-order/note/<str:number>/',
         views.CommentUpdateView.as_view(), name='update-order-note'),
    path('update/active-order/internal-note/<str:number>/',
         views.InternalNoteUpdateView.as_view(), name='update-order-internal-note'),

]
