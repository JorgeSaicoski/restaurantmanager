from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# To create many restaurants.
class Restaurant(models.Model):
    name = models.CharField(max_length=200, default="")
    #how can add products and change the cash?
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #restaurant image
    image = models.ImageField(null=False, blank=True, upload_to='restaurant/', default="/default/restaurant.png")
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
    #how much order this restaurant have today?
    counter = models.IntegerField(default=1)
    #description
    description = models.TextField(max_length=2000, default="")
    #contact for clients
    contact = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name
    #here we will get and check all the staff
    @property
    def get_kitchen(self):
        list = []
        for i in self.kitchen.all():
            list.append(i)
        return list
    @property
    def get_weiter(self):
        list = []
        for i in self.weiter.all():
            list.append(i)
        return list
    def get_cashier(self):
        list = []
        for i in self.cashier.all():
            list.append(i)
        return list
    def get_owner(self):
        list = [self.owner]
        return list



