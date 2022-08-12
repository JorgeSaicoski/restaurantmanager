from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True, default="")
	phone = models.IntegerField(default=0, null=True, blank=True)
	restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete = models.CASCADE)

	def __str__(self):
		return self.name
	#Get customer to print in the order for the weiter/delivery/tables
	@property
	def get_customer(self):
		name = self.name
		email = self.email
		phone = self.phone
		return {"name":name, "email":email, "phone":phone}

	#get orders to cashier
	@property
	def get_orders(self):
		orders = self.order_set.all().values()
		list = []
		order = []
		for i in orders:
			complete = i["complete"]
			closed = i["closed"]
			transaction_id = i["transaction_id"]
			delivery = i["delivery"]
			list.append({"complete":complete, "closed":closed, "transaction_id":transaction_id, "delivery":delivery})
		order.append({"orders":list,"customer":self.get_customer})
		return order
