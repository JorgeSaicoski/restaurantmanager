from django.shortcuts import render
from restaurants.models import Restaurant

# Create your views here.
def home(request):
    restaurants = Restaurant.objects.all()
    show_login = True
    if request.user.is_authenticated:
        show_login = False
    context = {
        'restaurants': restaurants,
        'show_login': show_login,
	}
    return render(request, 'restaurants/home.html', context)