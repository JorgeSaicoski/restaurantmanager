from django.shortcuts import render
from restaurants.models import Restaurant
from store.models import OrderItem, Order, Product
from django.http import JsonResponse
import json


# Create your views here.

def list(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'staff/list.html', context)


def main(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    is_kitchen = False
    # check if user is auth to kitchen
    if request.user in restaurant.get_kitchen:
        is_kitchen = True
    context = {
        'restaurant': restaurant,
        'is_kitchen': is_kitchen,
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
    #check if the orders is completed
    todo = []
    #loop to get the dictonary in the order
    for i in order.get_items:
        todo.append(i)
    for i in todo:
        if i["complete"] is False:
            order.complete = False
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
            if i.complete:
                info.append(i.get_items_order)
            else:
                todo.append(i.get_items_order)

    print(info)
    context = {
        'restaurant': restaurant,
        'todo': todo,
        'info': info,
    }
    return render(request, 'staff/weiter.html', context)
