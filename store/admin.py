from typing import Any
from django.contrib import admin
from store.models import Cart, CartItem, Collection, Order, OrderItem, Product, ProductImage

# Register your models here.


class ProductImageInlineAdmin(admin.TabularInline):
    model = ProductImage
    extra = 2
    max_num = 5
    min_num = 1
    list_display = ('id', 'product', "image")


class StatusFilter(admin.SimpleListFilter):
    title = "Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("low", "Low"),
            ("high", "High")
        ]

    def queryset(self, request, queryset):
        if self.value() == "low":
            return queryset.filter(inventory__lt=10)
        if self.value() == "high":
            return queryset.filter(inventory__gt=19)


@admin.register(Product)
class PrdouctAdmin(admin.ModelAdmin):
    actions = ("clear_inventory_action",)
    list_display = ('name', 'unit_price', 'inventory', 'status')
    list_filter = (StatusFilter, )
    search_fields = ('name',)
    inlines = (ProductImageInlineAdmin,)

    @admin.display(ordering='inventory')
    def status(self, product):
        if product.inventory < 10:
            return "Low"
        elif product.inventory >= 10 and product.inventory < 20:
            return "OK"

        return "High"

    @admin.action(description="Clear inventory")
    def clear_inventory_action(self, request, queryset):
        queryset.update(inventory=0)
        self.message_user(request, "Successfully cleared inventory!")


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'featured_product')


class CartItemInlineAdmin(admin.TabularInline):
    model = CartItem
    extra = 2


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ('id',)
    inlines = (CartItemInlineAdmin,)


class OrderItemInlineAdmin(admin.TabularInline):
    model = OrderItem
    extra = 2


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('id',)
    inlines = (OrderItemInlineAdmin,)
