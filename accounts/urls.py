from django.urls import path

from . import views

urlpatterns = [
	path('register/', views.register_request, name="register"),
	path('register/customer', views.customer_request, name="customer_register"),
]
