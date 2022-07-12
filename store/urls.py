from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	#Change to get a specif restaurant
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

]