from django.contrib import admin
from restaurants.models import Restaurant
from store.models import Order
from store.admin import ProductInLine
# Register your models here.

class OrderInLine(admin.StackedInline):
    model = Order

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductInLine, OrderInLine]

admin.site.register(Restaurant,RestaurantAdmin)