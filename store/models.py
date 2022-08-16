from django.db import models
from restaurants.models import Restaurant
from accounts.models import Customer
# Create your models here.




class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	description = models.TextField(max_length=2000, default="")
	image = models.ImageField(null=False, blank=True, upload_to='restaurant/',default="/default/food.svg")
	def __str__(self):
		return self.name
	#Get te properties when it is needed
	@property
	def get_name(self):
		return self.name
	@property
	def get_price(self):
		return self.price


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
