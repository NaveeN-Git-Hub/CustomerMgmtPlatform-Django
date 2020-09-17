from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:id>/', views.customer, name='customer'),
    path('create_order/', views.create_order, name='create_order'),
    path('update_order/<str:id>', views.update_order, name='update_order'),
    path('remove_order/<str:id>', views.remove_order, name='remove_order'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

]
