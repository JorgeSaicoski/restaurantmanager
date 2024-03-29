from django.shortcuts import render, redirect
from accounts.models import Customer
from store.models import Order, ShippingAddress
# Create your views here.
def user_list(request, pk):
    # Change to get a specif restaurant
    if request.user.is_authenticated:
        user = request.user
        # if the user havent a customer
        try:
            customer = Customer.objects.get(user=user)
            message = False
        except:
            return redirect("/account/register/customer")

    else:
        try:
            Customer.objects.get(email=pk).user
            print(user)
            return redirect("/account/login/")
        except:
            customer = Customer.objects.get(email=pk)
            message = "para proteger esta pagina, registre con el mismo e-mail del pedido"

    orders = Order.objects.filter(customer=customer).order_by('-date_ordered')
    context = {
        'customer':customer,
        'orders': orders,
        'message': message,
    }
    return render(request, 'orders/list.html', context)

def order_detail(request, pk, email):
    order = Order.objects.get(id=pk)

    shipping = ShippingAddress.objects.get(order=order).get_shipping


    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get(user=user)
    else:
        customer = Customer.objects.get(email=email)

    if order.customer == customer:
        return render(request, 'orders/order.html', {'order': order, 'customer': customer, 'shipping': shipping,})
    else:
        if request.user.is_authenticated:
            orders = Order.objects.filter(customer=customer).order_by('-date_ordered')
            message = "no tenes permisso a este pedido"
            context = {
                'customer': customer,
                'orders': orders,
                'message': message,
            }
            return render(request, 'orders/list.html', context)
        return redirect("/account/login")



