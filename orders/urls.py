from django.urls import path

from . import views
urlpatterns = [
	path('<str:pk>/', views.user_list, name="orders"),
]
