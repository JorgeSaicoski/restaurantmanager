from django.urls import path

from . import views

urlpatterns = [
	path('', views.list, name="list"),
	path('<str:pk>/', views.main, name="main"),
	path('<str:pk>/cocina', views.kitchen, name="kitchen"),
	path('<str:pk>/update_item/', views.update_item, name="update_item"),
]
