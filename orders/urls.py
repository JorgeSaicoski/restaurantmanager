from django.urls import path

from . import views
urlpatterns = [
	path('<str:pk>/', views.user_list, name="orders"),
	path('<str:email>/pedido/<str:pk>/', views.order_detail, name="orders"),
]
