from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	#Change to get a specif restaurant
	path('<str:pk>/', views.store, name="store"),
	path('<str:pk>/cart/', views.cart, name="cart"),
	path('<str:pk>/checkout/', views.checkout, name="checkout"),
	path('<str:pk>/update_item/', views.updateItem, name="update_item"),
	path('<str:pk>/process_order/', views.processOrder, name="process_order"),
]
