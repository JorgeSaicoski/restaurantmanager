from django.shortcuts import render
from accounts.models import Customer
from store.models import Order
# Create your views here.
def user_list(request, pk):
    # Change to get a specif restaurant
    if request.user.is_authenticated:
        user = request.user.customer
        customer =  Customer.objects.get(user=user)
    else:
        try:
            customer = Customer.objects.get(email=pk)
        except:
            return render(request, 'orders/identify.html', context)
    orders = Order.objects.filter(customer=customer)
    context = {
        'customer':customer,
        'orders': orders,
    }
    return render(request, 'orders/list.html', context)

def order_detail(request, pk, email):
    order = Order.objects.get(id=pk)

    if request.user.is_authenticated:
        user = request.user.customer
        customer = Customer.objects.get(user=user)
    else:
        customer = Customer.objects.get(email=email)

    if order.customer = customer:
        return render(request, 'orders/order.html', {'orders': orders})
    else:
        return render(request, 'orders/identify.html', context)



