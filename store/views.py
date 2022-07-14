from django.shortcuts import render
from restaurants.models import Restaurant
from store.models import Product, Order, OrderItem
from django.http import JsonResponse
import json
# Create your views here.
#go to store
def store(request,pk):
	# Change to get a specif restaurant
	restaurant = Restaurant.objects.get(name=pk)
	products = Product.objects.filter(restaurant=restaurant)
	context = {
		'restaurant':restaurant,
		'products':products
	}
	return render(request, 'store.html', context)

#send to cart
def cart(request, pk):
	restaurant = Restaurant.objects.get(name=pk)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False, restaurant=restaurant)
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

#send to pay
def checkout(request,pk):
	restaurant = Restaurant.objects.get(name=pk)
	context = {
		'restaurant': restaurant,
	}
	return render(request, 'checkout.html', context)

# link to update items in the cart
def updateItem(request, pk):
	restaurant = Restaurant.objects.get(name=pk)

	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False, restaurant=restaurant)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()
		
	return JsonResponse('Item was added', safe=False)
