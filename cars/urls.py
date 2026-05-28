from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/create/', views.car_create, name='car_create'),
    path('car/<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('car/<int:pk>/delete/', views.car_delete, name='car_delete'),
    path('car/<int:pk>/toggle-active/', views.car_toggle_active, name='car_toggle_active'),
    path('car/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('brands/', views.brand_list, name='brand_list'),
    path('api/models/', views.get_models, name='get_models'),
    path('chat/<int:car_pk>/<int:user_pk>/', views.chat, name='chat'),
    path('chats/', views.my_chats, name='my_chats'),
]