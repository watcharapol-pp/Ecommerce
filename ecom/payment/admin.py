from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register your models here.
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'amount', 'status', 'created_at')
#     search_fields = ('status',)

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)