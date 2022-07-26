from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# To create many restaurants.
class Restaurant(models.Model):
    name = models.CharField(max_length=200, default="")
    #how can add products and change the cash?
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #how can create order
    weiter = models.ManyToManyField(User, related_name="weiter")
    #how receive the order and change this state?
    kitchen = models.ManyToManyField(User, related_name="kitchen")
    #how can close a order?
    cashier = models.ManyToManyField(User, related_name="cashier")
    #how much the restaurant have in the cash?
    cash = models.FloatField()
    #this restaurant paid us?
    is_vip = models.BooleanField(default=True)
    #30 days free. And then the restaurant must to pay to renew. Manualy check is cheaper.
    vip_days = models.IntegerField(default=30)

    def __str__(self):
        return self.name
    @property
    def get_kitchen(self):
        list = []
        for i in self.kitchen.all():
            list.append(i)
        return list

