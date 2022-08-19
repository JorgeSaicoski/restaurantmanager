from django.contrib import admin
from store.models import Customer, Product, Order, OrderItem, ShippingAddress, Category
# Register your models here.

#preparing to put on Restaurant admin
class ProductInLine(admin.StackedInline):
    model = Product
#preparing to put on Order Admin
class OrderItemInLine(admin.StackedInline):
    model = OrderItem
#to be easy to search the restaurant that own the product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
#to be easy to see what product is on the order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'restaurant', 'date_ordered', 'complete', 'closed')
    list_editable = ('complete', 'closed')
    inlines = [OrderItemInLine,]

admin.site.register(Customer)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(ShippingAddress)
