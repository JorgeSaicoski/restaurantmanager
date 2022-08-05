from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	phone = models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return self.name
	#Get customer to print in the order for the weiter/delivery
	@property
	def get_customer(self):
		name = self.name
		email = self.email
		phone = self.phone
		return {"name":name, "email":email, "phone":phone}