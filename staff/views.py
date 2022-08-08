from django.shortcuts import render
from restaurants.models import Restaurant
from store.models import OrderItem, Order, Product
from django.http import JsonResponse
import json


# Create your views here.

# Function to check the permission


# List of restaurants
def list(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'staff/list.html', context)

# Get the list of permission that this user have.
def main(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    # Initially it have no permissions.
    is_kitchen = False
    is_weiter = False
    # Now we check the permissions
    # check if user is auth to kitchen
    if request.user in restaurant.get_kitchen:
        is_kitchen = True
    # check if user is auth to weiter
    if request.user in restaurant.get_weiter:
        is_weiter = True
    context = {
        'restaurant': restaurant,
        'is_kitchen': is_kitchen,
        'is_weiter': is_weiter,
    }
    return render(request, 'staff/main.html', context)

def kitchen(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    #get the orders of this restaurant
    orders = Order.objects.filter(restaurant=restaurant)
    todo = []
    # check if user is auth to kitchen
    if request.user in restaurant.get_kitchen:
        #get the todo itens (will get only the todo itens for this restaurant)
        for i in orders:
            #function to detail any item for a order
            product = i.get_items
            #loop for get only dictonary
            for i in product:
                todo.append(i)

    context = {
        'restaurant': restaurant,
        'todo': todo,
        'is_kitchen': True,
        'is_weiter': True,
    }
    return render(request, 'staff/kitchen.html', context)

def update_item(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    orderId = data['orderId']
    product = Product.objects.get(id=productId)
    order = Order.objects.get(transaction_id=orderId)
    orderItem = OrderItem.objects.get(order=order, product=product)
    if action == 'finish':
        orderItem.complete = True
    elif action == 'return':
        orderItem.complete = False
    orderItem.save()

    todo = []
    #loop to get the dictonary in the order
    for i in order.get_items:
        todo.append(i)
    # check if the orders is completed
    for i in todo:
        # if any item is not complete:
        if i["complete"] is False:
            #Order is not complete
            order.complete = False
            #And we dont need to check the rest
            break
        else:
            order.complete = True
            order.save()
    return JsonResponse('Item was added', safe=False)

def weiter(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    #get the orders of this restaurant
    orders = Order.objects.filter(restaurant=restaurant)
    info = []
    todo = []
    # check if user is auth to kitchen
    if request.user in restaurant.get_weiter:
        #get the todo itens (will get only the todo itens for this restaurant)
        for i in orders:
            #Separate the cart that is already paid to the cart that is not paid
            if i.complete:
                info.append(i.get_items_order)
            # The order that is not paid the weiter can change (put and sack products)
            else:
                todo.append(i.get_items_order)

    context = {
        'restaurant': restaurant,
        'todo': todo,
        'info': info,
        'is_kitchen': True,
        'is_weiter': True,
    }
    return render(request, 'staff/weiter.html', context)
