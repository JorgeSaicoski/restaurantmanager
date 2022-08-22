from django.urls import path

from . import views

urlpatterns = [
	path('register/', views.register_request, name="register"),
	path('customer/', views.customer_request, name="customer_page"),
	path('login/', views.login_request, name="login"),
	path('logout/', views.logout_request, name="logout"),
	path('customer/update', views.updateCustomer, name="customer_update"),
]
