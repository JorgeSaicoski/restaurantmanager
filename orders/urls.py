from django.urls import path

from . import views
urlpatterns = [
	path('<str:pk>/', views.user_list, name="orders_customer"),
	path('<str:email>/pedido/<str:pk>/', views.order_detail, name="orders_customer_detail"),
]
