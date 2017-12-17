from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    #fields = ('first_name', 'last_name')
    list_display = ('username', 'full_name', 'birthday', 'count_of_orders', 'img',)
    list_filter = ('sex',)
    search_fields = ['last_name', 'first_name']

    def full_name(self, obj):
        return "{} {}".format(obj.last_name, obj.first_name)

    def username(self, obj):
        return "{}".format(obj.user.username)

    def count_of_orders(self, obj):
        ord = Order.objects.filter(user=obj)
        return len(ord)


@admin.register(Prodact)
class ProdactAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('prodact','price','description', 'img',)
    list_filter = ('price',)
    search_fields = ['prodact_name']

    def prodact(self, obj):
        return "{}".format(obj.prodact_name)

    def price(self, obj):
        return "{}".format(obj.price)

    def description(self, obj):
        return "{}".format(obj.description)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('username', 'prodact', 'date')
    list_filter = ('prodact__prodact_name',)
    search_fields = ['prodact__prodact_name']

    def username(self, obj):
        return "{}".format(obj.user.user)

    def date(self, obj):
        return "{}".format(obj.order_date)


@admin.register(ProdactCategory)
class ProdactCategoryAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('category_name',)