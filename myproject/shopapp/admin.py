from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from shopapp.admin_mixins import ExportAsCSVMixin
from shopapp.common import save_csv_products, save_csv_orders
from shopapp.forms import CSVImportForm
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
    change_list_template = 'shopapp/products_changelist.html'

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context=context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context=context, status=400)

        save_csv_products(
            file=form.files['csv_file'].file,
            encoding=request.encoding
        )
        self.message_user(request, 'Products from CSV was imported.')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-products-csv/', self.import_csv, name='import-products-csv')
        ]
        return new_urls + urls


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # inlines = [
    #     OrderStackedInline,
    # ]
    list_display = 'id', 'delivery_address', 'user'
    list_display_links = 'id', 'delivery_address'
    search_fields = 'delivery_address',
    change_list_template = 'shopapp/orders_changelist.html'

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context=context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context=context, status=400)
        save_csv_orders(
            file=form.files['csv_file'].file,
            encoding=request.encoding
        )
        self.message_user(request, 'Orders from CSV was imported.')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-orders-csv/', self.import_csv, name='import-orders-csv')
        ]
        return new_urls + urls
