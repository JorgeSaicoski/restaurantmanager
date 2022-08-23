from django.urls import path

from . import views

urlpatterns = [
	path('', views.list, name="list"),
	path('<str:pk>/', views.main, name="main"),
	path('<str:pk>/cocina/', views.kitchen, name="kitchen"),
	path('<str:pk>/cashier/', views.cashier, name="cashier"),
	path('<str:pk>/mozo/', views.weiter, name="weiter"),
	path('<str:pk>/owner/', views.owner, name="owner"),
	path('<str:pk>/update_item/', views.update_item, name="update_item"),
	path('<str:pk>/delivery_item/', views.delivery_item, name="delivery_item"),
	path('<str:pk>/new_table/', views.new_table, name="new_table"),
	path('<str:pk>/new_product/', views.new_product, name="new_product"),
	path('<str:pk>/tables/', views.tables, name="tables"),
	path('<str:pk>/create/<str:table>/', views.table, name="table"),
	path('<str:pk>/pedidos/<str:id>/', views.orderDetail, name="orderDetail"),
	path('<str:pk>/<str:table>/update_table/', views.updateTable, name="update_table"),
	path('<str:pk>/<str:id>/update_order/', views.updateOrder, name="update_order"),
	path('<str:pk>/restaurant_update/', views.restaurant_update, name="restaurant_update"),
	path('<str:pk>/<str:table>/process_table/', views.processTable, name="process_table"),
	path('<str:pk>/<str:id>/close_order/', views.closeOrder, name="close_order"),

]
