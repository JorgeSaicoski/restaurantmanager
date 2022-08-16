from django.db import models


# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=1000, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    delivery = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    # get the price to buy this orden (to help in cart)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    # Get cart items to print in cart
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    # Get cart items to print to kitchen
    @property
    def get_items(self):
        orderitems = self.orderitem_set.all().values()
        list = []
        for i in orderitems:
            id = i["product_id"]
            order_id = self.transaction_id
            complete = i["complete"]
            delivered = i["delivered"]
            quantity = i["quantity"]
            product = Product.objects.get(id=i["product_id"])
            product_name = product.get_name
            list.append({'product_id': id, 'order_id': order_id, 'complete': complete, 'quantity': quantity,
                         'product_name': product_name, 'delivered': delivered})
        return list

    @property
    def is_delivery(self):
        return self.delivery

    # if all itens is completed (for weiter)
    @property
    def is_finished(self):
        orderitems = self.orderitem_set.all().values()
        for item in orderitems:
            if not item["delivered"]:
                return False
        return True

    # Get cart items to print to weiter
    @property
    def get_items_order(self):
        order = []
        if self.delivery:
            shipping_address = ShippingAddress.objects.filter(order=self.id)

            for i in shipping_address:
                shipping = i.get_shipping
                order.append({"shipping": shipping})

        else:
            order.append({"shipping": False})

        items = self.get_items
        custumer = self.customer.get_customer
        order.append({"items": items, "customer": custumer})
        return order


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)

    # get how much is to buy this product in this order
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
