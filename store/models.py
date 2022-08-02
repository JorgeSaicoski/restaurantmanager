from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	phone = models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	@property
	def get_name(self):
		return self.name
	@property
	def get_price(self):
		return self.price

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	closed = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	delivery = models.BooleanField(default=True)

	def __str__(self):
		return str(self.id)
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	@property
	def get_items(self):
		orderitems = self.orderitem_set.all().values()
		list = []
		for i in orderitems:
			id = i["product_id"]
			order_id = i["order_id"]
			complete = i["complete"]
			quantity = i["quantity"]
			product = Product.objects.get(id=i["product_id"])
			product_name = product.get_name
			list.append({'product_id': id, 'order_id': order_id, 'complete': complete, 'quantity':quantity, 'product_name':product_name})
		return list
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	def __str__(self):
		return str(self.product)
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
