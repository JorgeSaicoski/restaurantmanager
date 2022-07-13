from django.shortcuts import render
from restaurants.models import Restaurant
from store.models import Product, Order, OrderItem
# Create your views here.
def store(request,pk):
	# Change to get a specif restaurant
	restaurant = Restaurant.objects.get(name=pk)
	products = Product.objects.filter(restaurant=restaurant)
	context = {
		'restaurant':restaurant,
		'products':products
	}
	return render(request, 'store.html', context)

def cart(request, pk):
	restaurant = Restaurant.objects.get(name=pk)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0,'get_cart_items':0}

	context = {
		'items':items,
		'order':order,
		'restaurant':restaurant,
	}
	return render(request, 'cart.html', context)


def checkout(request,pk):
	restaurant = Restaurant.objects.get(name=pk)
	context = {
		'restaurant': restaurant,
	}
	return render(request, 'checkout.html', context)