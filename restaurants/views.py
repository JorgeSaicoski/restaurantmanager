from django.shortcuts import render
from restaurants.models import Restaurant

# Create your views here.
def home(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
	}
    return render(request, 'restaurants/home.html', context)