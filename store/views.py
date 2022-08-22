from django.shortcuts import render, redirect
from restaurants.models import Restaurant
from store.models import Product, Order, OrderItem, ShippingAddress, Category
from django.http import JsonResponse
import json
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
#go to store
def store(request,pk):
	# Change to get a specif restaurant
	restaurant = Restaurant.objects.get(name=pk)
	categories = Category.objects.all()
	products = Product.objects.filter(restaurant=restaurant)
	categories_list = []
	for i in categories:
		check = i.get_products
		put = False
		for product_check in check:
			if product_check in products:
				put = True
		if put:
			categories_list.append(i)




	#get cookies
	# if the user havent a customer
	try:
		data = cartData(request, restaurant)
	except:
		return redirect("/account/register/customer")
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	if request.user.is_authenticated:
		items = order.get_items



	context = {'products':products, 'cartItems':cartItems, 'restaurant':restaurant, 'order':order, 'categories':categories_list, "items":items}
	return render(request, 'store/store.html', context)

def store_category(request,pk,category):
	# Change to get a specif restaurant
	restaurant = Restaurant.objects.get(name=pk)
	category_select = Category.objects.get(name=category.title())
	products = Product.objects.filter(restaurant=restaurant, category=category_select)

	#get cookies
	# if the user havent a customer
	try:
		data = cartData(request, restaurant)
	except:
		return redirect("/account/customer/")
	cartItems = data['cartItems']
	order = data['order']

	context = {'products':products, 'cartItems':cartItems, 'restaurant':restaurant, 'order':order, 'categories':[category_select]}
	return render(request, 'store/store.html', context)

#send to cart
def cart(request, pk):
	restaurant = Restaurant.objects.get(name=pk)
	if request.user.is_authenticated:

		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, closed=False, complete=False, restaurant=restaurant)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']
		for i in cart:
			# We use try block to prevent items in cart that may have been removed from causing error
			try:
				cartItems += cart[i]['quantity']
				product = Product.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']
				item = {
					'id': product.id,
					'product': {'id': product.id, 'name': product.name, 'price': product.price}, 'quantity': cart[i]['quantity'],
					'get_total': total,
				}
				items.append(item)
			except:
				pass

	context = {
		'items':items,
		'order':order,
		'restaurant':restaurant,
		'cartItems':cartItems
	}
	return render(request, 'store/cart.html', context)

#send to pay
def checkout(request,pk):
	restaurant = Restaurant.objects.get(name=pk)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, closed=False, complete=False, restaurant=restaurant)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		data = cartData(request, restaurant)
		cartItems = data['cartItems']
		order = data['order']
		items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems, 'restaurant':restaurant}
	return render(request, 'store/checkout.html', context)

# link to update items in the cart
def updateItem(request, pk):
	restaurant = Restaurant.objects.get(name=pk)

	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, closed=False, complete=False, restaurant=restaurant)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request, pk):
	restaurant = Restaurant.objects.get(name=pk)


	#get form data
	data = json.loads(request.body)
	#if it is logged
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False, restaurant=restaurant)
	#if not logged
	else:
		customer, order = guestOrder(request, data, restaurant)

	#create id
	transaction_id = restaurant.counter

	restaurant.counter = restaurant.counter + 1
	restaurant.save()
	order.transaction_id = transaction_id

	order.complete = True
	order.save()

	#if it is delivery
	if order.delivery == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)


	return JsonResponse('Payment submitted..', safe=False)


