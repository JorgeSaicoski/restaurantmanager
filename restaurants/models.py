from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# To create many restaurants.
class Restaurant(models.Model):
    name = models.CharField(max_length=200, default="")
    #how can add products and change the cash?
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #how can create order
    weiter = models.ManyToManyField(User)
    #how receive the order and change this state?
    kitchen = models.ManyToManyField(User)
    #how can close a order?
    cashier = models.ManyToManyField(User)
    #how much the restaurant have in the cash?
    cash = models.FloatField()
    #this restaurant paid us?
    is_vip = models.BooleanField(default=True)
    #30 days free. And then the restaurant must to pay to renew. Manualy check is cheaper.
    vip_days = IntegerField(default=30)