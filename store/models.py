from django.db import models
from restaurants.models import Restaurant
from accounts.models import Customer
# Create your models here.



class Category(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField(null=False, blank=True, upload_to='category/')
	def __str__(self):
		return self.name
	@property
	def get_products(self):
		products = Product.objects.filter(category=self.id)
		return products

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, editable=False)
	description = models.TextField(max_length=2000, default="", null=False, blank=True)
	category = models.ManyToManyField(Category, related_name="category")
	image = models.ImageField(null=True, blank=True, upload_to='restaurant/', default="/default/food.svg")
	def __str__(self):
		return self.name
	#Get te properties when it is needed
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
	transaction_id = models.CharField(max_length=1000, null=True, blank=True)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	delivery = models.BooleanField(default=True)

	def __str__(self):
		return str(self.id)
	#get the price to buy this orden (to help in cart)
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	#Get cart items to print in cart
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	#Get cart items to print to kitchen
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
			order_item = OrderItem.objects.get(order=self, product=product)
			total = order_item.get_total
			list.append({'product_id': id, 'order_id': order_id, 'complete': complete, 'quantity':quantity, 'product_name':product_name, 'delivered':delivered,"total":total})
		return list

	@property
	def is_delivery(self):
		return self.delivery
	#if all itens is completed (for weiter)
	@property
	def is_finished(self):
		orderitems = self.orderitem_set.all().values()
		for item in orderitems:
			if not item["delivered"]:
				return False
		return True
	# Get cart info to print to weiter
	@property
	def get_order_info(self):
		order = []
		if self.delivery:
			shipping_address = ShippingAddress.objects.filter(order=self.id)

			for i in shipping_address:
				shipping = i.get_shipping
				order.append({"shipping": shipping})

		else:
			order.append({"shipping": False})


		custumer = self.customer.get_customer
		order.append({"customer":custumer})
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
	#get how much is to buy this product in this order
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

	# Get shipping to print in the order for the weiter/delivery
	@property
	def get_shipping(self):
		address = self.address
		city = self.city
		return {"address":address,"city":city}
