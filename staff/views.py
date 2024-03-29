from django.shortcuts import render, redirect, get_object_or_404
from restaurants.models import Restaurant
from store.models import OrderItem, Order, Product, ShippingAddress, Category
from .forms import NewTableForm, NewProdutcForm, UptadeRestaurant, UptadeProduct
from accounts.models import Customer
from django.http import JsonResponse
import json


# Create your views here.

# Function to check the permission
def is_kitchen(user, restaurant):
    if user in restaurant.get_kitchen:
        return True
    else:
        return False


def is_weiter(user, restaurant):
    if user in restaurant.get_weiter:
        return True
    else:
        return False


def is_cashier(user, restaurant):
    if user in restaurant.get_cashier():
        return True
    else:
        return False


def is_owner(user, restaurant):
    if user in restaurant.get_owner():
        return True
    else:
        return False


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
    user = request.user
    context = {
        'restaurant': restaurant,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant)
    }
    return render(request, 'staff/main.html', context)


def kitchen(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    # get the orders of this restaurant
    orders = Order.objects.filter(restaurant=restaurant, closed=False).order_by('transaction_id')
    user = request.user
    local = []
    delivery = []
    # check if user is auth to kitchen
    if is_kitchen(user, restaurant) or is_owner():
        # get the todo itens (will get only the todo itens for this restaurant)

        for i in orders:
            if i.transaction_id:
                # function to detail any item for a order
                if i.is_delivery:
                    product = i.get_items
                    delivery.append(product)
                else:
                    product = i.get_items
                    local.append(product)

    context = {
        'restaurant': restaurant,
        'local': local,
        'delivery': delivery,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant)
    }
    return render(request, 'staff/kitchen.html', context)


# Kitchen update item for weiter delivery
def update_item(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    orderId = data['orderId']
    product = Product.objects.get(id=productId)
    order = Order.objects.get(transaction_id=orderId, restaurant=restaurant)
    orderItem = OrderItem.objects.get(order=order, product=product)
    if action == 'finish':
        orderItem.complete = True
    elif action == 'return':
        orderItem.complete = False
        orderItem.delivered = False
    orderItem.save()

    todo = []
    # loop to get the dictonary in the order
    for i in order.get_items:
        todo.append(i)
    return JsonResponse('Item was added', safe=False)


def cashier(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    user = request.user
    orders = []
    local_order = []
    customers_list = Customer.objects.filter(restaurant=restaurant)
    all_orders = Order.objects.filter(restaurant=restaurant, closed=False)
    if is_cashier(user, restaurant) or is_owner(user, restaurant):
        for customer in customers_list:
            list = []
            orders_customer = customer.get_orders
            custo = orders_customer[0]["customer"]["name"]
            for i in orders_customer[0]["orders"]:
                transaction_id = i["transaction_id"]
                this_orders = Order.objects.filter(restaurant=restaurant, transaction_id=transaction_id)
                for item in this_orders:
                    list.append(item)

            local_order.append({"name": custo, "item": list})
        for order in all_orders:
            if order.complete and order.delivery:
                orders.append(order)
    context = {
        'local_order': local_order,
        'orders': orders,
        'restaurant': restaurant,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant)
    }

    return render(request, 'staff/cashier.html', context)


def weiter(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    user = request.user
    # get the orders of this restaurant
    orders = Order.objects.filter(restaurant=restaurant, closed=False)
    info = []
    todo = []
    # check if user is auth to kitchen
    if is_weiter(user, restaurant) or is_owner(user, restaurant):
        # get the todo itens (will get only the todo itens for this restaurant)
        for i in orders:
            # Separate the cart that is already paid to the cart that is not paid
            if i.complete:
                if i.is_delivery:
                    if i.get_items:
                        info.append(i)
            # The order that is not paid the weiter can change (put and sack products)
    context = {
        'restaurant': restaurant,
        'todo': todo,
        'info': info,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant)
    }
    return render(request, 'staff/weiter.html', context)


# Owner page
def owner(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    user = request.user
    # check if user is auth to kitchen
    if is_owner(user, restaurant):
        # get the orders of this restaurant
        orders = Order.objects.filter(restaurant=restaurant).order_by('-date_ordered')

    context = {
        'restaurant': restaurant,
        "orders": orders,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant)
    }
    return render(request, 'staff/owner.html', context)


# Owner forms!!
# Create new product
def new_product(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    form = NewProdutcForm(request.POST)
    user = request.user
    if is_owner(user, restaurant):
        if request.method == "POST":
            # get information
            name = request.POST["name"]
            price = request.POST["price"]
            description = request.POST["description"]
            categories = request.POST["category"]
            # list to add category correctly
            category = []
            for i in categories:
                cat = Category.objects.get(id=i)
                category.append(cat)
            # create product and add category (restaurant add too)
            try:
                Product.objects.get(name=name, restaurant=restaurant)
                return render(request=request, template_name="staff/newproduct.html",
                              context={"form": form, "message": "Este producto ya existe"})
            except:
                pass
            product = Product.objects.create(name=name, price=price, restaurant=restaurant, description=description)
            product.category.set(category)
            return redirect("/staff/{}".format(restaurant))

        return render(request=request, template_name="staff/newproduct.html", context={"form": form})
    # if it is not owner:
    restaurant = Restaurant.objects.get(name=pk)
    context = {
        'restaurant': restaurant,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant),
        "message": "No tenes permiso para crear un producto",
    }
    return render(request, 'staff/main.html', context)


# Upgrade restaurant info
def restaurant_update(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    user = request.user

    context = {
        'restaurant': restaurant,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant),
        "message": "",
        'form': False,
    }

    if is_owner(user, restaurant):
        instance = get_object_or_404(Restaurant, name=pk)
        form = UptadeRestaurant(request.POST or None, instance=instance)
        context["form"] = form
        if form.is_valid():
            form.save()
            return redirect("/staff/{}/owner".format(restaurant))
        return render(request, 'staff/updaterestaurant.html', context)
    # if it is not owner:
    message = "No tenes permiso para crear un producto"
    context["message"] = message

    return render(request, 'staff/main.html', context)


# Uptade products:
def product_list(request, pk):
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
    for b in products:
        print(b.id)
    context = {'products': products, 'restaurant': restaurant, 'categories': categories_list}
    return render(request, 'staff/productlist.html', context)
def product_update(request, pk):

    product = Product.objects.get(id=pk)
    restaurant = product.restaurant
    user = request.user

    context = {
        'restaurant': restaurant,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant),
        "message": "",
        'form': False,
    }

    if is_owner(user, restaurant):
        instance = get_object_or_404(Product, id=pk)
        form = UptadeProduct(request.POST or None, instance=instance)
        context["form"] = form
        if form.is_valid():
            form.save()
            return redirect("/staff/{}/owner".format(restaurant))
        return render(request, 'staff/updateproduct.html', context)
    # if it is not owner:
    message = "No tenes permiso para crear un producto"
    context["message"] = message

    return render(request, 'staff/main.html', context)

# detail of a order
def orderDetail(request, pk, id):
    restaurant = Restaurant.objects.get(name=pk)
    user = request.user
    if is_weiter(user, restaurant) or is_owner(user, restaurant) or is_cashier(user, restaurant):
        order = Order.objects.get(transaction_id=id, restaurant=restaurant)
        customer = order.customer.get_customer
        products = Product.objects.filter(restaurant=restaurant)
        items = []
        for item in products:
            check = True
            for i in order.get_items:
                if item.get_name == i["product_name"]:
                    check = False
            if check:
                items.append(item)

        try:
            shipping = ShippingAddress.objects.get(order=order).get_shipping
        except:
            shipping = False
    context = {
        'items': items,
        'restaurant': restaurant,
        'order': order,
        'customer': customer,
        'shipping': shipping,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant)
    }
    return render(request, 'staff/orderdetail.html', context)


def delivery_item(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    data = json.loads(request.body)
    productId = data['productId']
    orderId = data['orderId']
    mode = data["mode"]
    order = Order.objects.get(transaction_id=orderId, restaurant=restaurant)
    product = Product.objects.get(id=productId)
    if mode == "item":
        orderItem = OrderItem.objects.get(order=order, product=product)
        orderItem.delivered = True
        orderItem.save()
    else:
        ordemItem = OrderItem.objects.filter(order=order)
        for item in ordemItem:
            item.delivered = True
            item.complete = True
            item.save()

    return JsonResponse('Item was added', safe=False)


def new_table(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    if request.method == "POST":
        form = NewTableForm(request.POST)
        if form.is_valid():
            name = request.POST["name"]
            try:
                customer = Customer.objects.get(name=name, restaurant=restaurant)
                return render(request=request, template_name="staff/newtable.html",
                              context={"register_form": form, "message": "Esta mesa ya existe"})
            except:
                customer = Customer.objects.create(name=name, restaurant=restaurant)
            customer.save()
            return redirect("/staff/{}/create/{}".format(restaurant, name))
    form = NewTableForm(request.POST)
    return render(request=request, template_name="staff/newtable.html", context={"register_form": form})


def tables(request, pk):
    restaurant = Restaurant.objects.get(name=pk)
    user = request.user
    tables = []
    if is_weiter(user, restaurant) or is_owner(user, restaurant):
        get_tables = Customer.objects.filter(restaurant=restaurant)
        for i in get_tables:
            tables.append(i.get_customer)

    context = {
        'restaurant': restaurant,
        'tables': tables,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant)
    }
    return render(request, 'staff/table.html', context)


def table(request, pk, table):
    restaurant = Restaurant.objects.get(name=pk)
    user = request.user
    orders_closed = []
    if is_weiter(user, restaurant) or is_owner(user, restaurant):

        customer = Customer.objects.get(name=table, restaurant=restaurant)
        table_detail = customer.get_customer
        order, created = Order.objects.get_or_create(customer=customer, closed=False, complete=False, delivery=False,
                                                     restaurant=restaurant)
        products = Product.objects.filter(restaurant=restaurant)
        orders_closed = Order.objects.filter(customer=customer, closed=False, complete=True, restaurant=restaurant)
        items = []
        for item in products:
            check = True
            for i in order.get_items:
                if item.get_name == i["product_name"]:
                    check = False
            if check:
                items.append(item)

    context = {
        'items': items,
        'table': table_detail["name"],
        'restaurant': restaurant,
        'order': order,
        'orders_closed': orders_closed,
        'is_kitchen': is_kitchen(user, restaurant),
        'is_weiter': is_weiter(user, restaurant),
        'is_cashier': is_cashier(user, restaurant),
        'is_owner': is_owner(user, restaurant)
    }
    return render(request, 'staff/tabledetail.html', context)


def updateOrder(request, pk, id):
    restaurant = Restaurant.objects.get(name=pk)

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    product = Product.objects.get(id=productId)
    order = Order.objects.get(restaurant=restaurant, transaction_id=id)

    try:
        orderItem = OrderItem.objects.get(order=order, product=product)
    except:
        orderItem = OrderItem.objects.create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def updateTable(request, pk, table):
    restaurant = Restaurant.objects.get(name=pk)

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = Customer.objects.get(name=table, restaurant=restaurant)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, closed=False, complete=False, delivery=False,
                                                 restaurant=restaurant)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processTable(request, pk, table):
    restaurant = Restaurant.objects.get(name=pk)
    data = json.loads(request.body)
    # get form data
    customer = Customer.objects.get(name=table, restaurant=restaurant)
    order, created = Order.objects.get_or_create(customer=customer, complete=False, restaurant=restaurant)

    # create id
    transaction_id = restaurant.counter

    restaurant.counter = restaurant.counter + 1
    restaurant.save()
    order.transaction_id = transaction_id

    order.complete = True
    order.save()

    return JsonResponse('Payment submitted..', safe=False)


def closeOrder(request, pk, id):
    restaurant = Restaurant.objects.get(name=pk)
    data = json.loads(request.body)
    name = data['customer']
    order = Order.objects.get(restaurant=restaurant, transaction_id=id)
    order.closed = True
    order.save()

    #update the cash in restaurant
    restaurant.cash = restaurant.cash + order.get_cart_total
    restaurant.save()
    # try to delete the Costumer. If it is not a local is will pass
    try:
        customer = Customer.objects.get(name=name, restaurant=restaurant)
        # if this customer have any open order it will not be deleted
        for order in customer.get_orders:
            for i in order["orders"]:
                if i["transaction_id"]:
                    if not i["closed"]:
                        return JsonResponse('Payment submitted..', safe=False)
        customer.delete()
    except:
        pass

    return JsonResponse('Payment submitted..', safe=False)
