from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from shopapp.admin_mixins import ExportAsCSVMixin
from shopapp.models import Product, Order, ProductImage


class ProductTabularInline(admin.TabularInline):
    model = Order.products.through


class ProductImageTabularInline(admin.StackedInline):
    model = ProductImage


class OrderStackedInline(admin.StackedInline):
    model = Product.orders.through



def archived_mark(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


def unarchived_mark(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    inlines = [
        ProductTabularInline,
        ProductImageTabularInline,
    ]
    actions = [
        archived_mark,
        unarchived_mark,
        'export_csv',
    ]
    list_display = 'id', 'name', 'price', 'archived'
    list_display_links = 'id', 'name'
    ordering = '-id',
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'preview'),

        }),
        ('Price Options', {
            'fields': ('price',),
            'classes': ('wide',),
        }),
        ('Extra Options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Field for a soft delete',
        })
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # inlines = [
    #     OrderStackedInline,
    # ]
    list_display = 'id', 'delivery_address', 'user'
    list_display_links = 'id', 'delivery_address'
    search_fields = 'delivery_address',

