from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from ficha.models import Product, Store, Order
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

