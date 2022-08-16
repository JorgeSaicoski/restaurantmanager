from django.shortcuts import render


# Create your views here.
def user_list(request, pk):
    # Change to get a specif restaurant
    if request.user.is_authenticated:
        customer = request.user.customer
    return render(request, 'store/store.html', context)
