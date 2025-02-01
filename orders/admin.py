from django.contrib import admin
from .models import Customer, Order

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone_number', 'user', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'code', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item', 'amount', 'created_at')
    list_filter = ('created_at', 'customer')
    search_fields = ('customer__name', 'item')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 20
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer')
