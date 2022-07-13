from django.contrib import admin
from store.models import Customer, Product, Order, OrderItem, ShippingAddress
# Register your models here.

class ProductInLine(admin.StackedInline):
    model = Product
class OrdemItemInLine(admin.StackedInline):
    model = OrderItem
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
class OrdemAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'restaurant', 'date_ordered', 'complete', 'closed')
    list_editable = ('complete', 'closed')
    inlines = [OrdemItemInLine,]

admin.site.register(Customer)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order, OrdemAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)