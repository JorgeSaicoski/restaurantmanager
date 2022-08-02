from django.shortcuts import render
from restaurants.models import Restaurant
from store.models import OrderItem, Order


# Create your views here.

def list(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'staff/list.html', context)


def main(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    orders = Order.objects.filter(restaurant=restaurant).values()
    is_kitchen = False
    # check if user is auth to kitchen
    if request.user in restaurant.get_kitchen:
        is_kitchen = True
        #get the itens to do
        todo = OrderItem.objects.filter(order__in=orders).values()

    context = {
        'restaurant': restaurant,
        'is_kitchen': is_kitchen,
        'todo': todo,
    }
    return render(request, 'staff/main.html', context)

def update_item(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    product = Product.objects.get(id=productId)
    order = Order.objects.get(customer=customer, closed=False, restaurant=restaurant)
    orderItem = OrderItem.objects.get(order=order, product=product)
    if action == 'finish':
        orderItem.complete = True
    elif action == 'return':
        orderItem.complete = False
    orderItem.save()
    #check if the orders is completed
    todo = OrderItem.objects.filter(order=order).values()
    for i in todo:
        if i.complete is false:
            pass
        else:
            order.complete = True
