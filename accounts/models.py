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


