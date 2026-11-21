from django.contrib import admin
from .models import FoodItem, Order, OrderItem, ContactMessage, TableBooking

admin.site.register(TableBooking)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)


admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderItem)