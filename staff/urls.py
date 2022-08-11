from django.urls import path

from . import views

urlpatterns = [
	path('', views.list, name="list"),
	path('<str:pk>/', views.main, name="main"),
	path('<str:pk>/cocina/', views.kitchen, name="kitchen"),
	path('<str:pk>/mozo/', views.weiter, name="weiter"),
	path('<str:pk>/update_item/', views.update_item, name="update_item"),
	path('<str:pk>/delivery_item/', views.delivery_item, name="delivery_item"),
	path('<str:pk>/new_table/', views.new_table, name="new_table"),
	path('<str:pk>/tables/', views.tables, name="tables"),
	path('<str:pk>/<str:table>/', views.table, name="table"),
	path('<str:pk>/<str:table>/update_table/', views.updateTable, name="update_table"),
	path('<str:pk>/<str:table>/process_table/', views.processTable, name="update_table"),
]
