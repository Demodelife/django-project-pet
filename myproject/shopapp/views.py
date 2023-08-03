import logging
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from shopapp.forms import ProductForm, GroupForm
from shopapp.models import Product, Order, ProductImage

logger = logging.getLogger(__name__)


# def shop_index(request: HttpRequest) -> HttpResponse:
#     context = {
#         'products': [
#             ('Apple', 150),
#             ('Pear', 200),
#             ('Mango', 500),
#         ],
#         'request': request,
#     }
#     return render(request, 'shopapp/index.html', context=context)

class ShopIndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'products': [
                ('Apple', 150),
                ('Pear', 200),
                ('Mango', 500),
            ],
            'request': request,
            'items': 1,
        }
        logger.debug('Products for shop index: {}'.format(context['products']))
        logger.info('Rendering shop index')
        return render(request, 'shopapp/index.html', context=context)


class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        groups = Group.objects.all()
        context = {
            'form': GroupForm(),
            'groups': groups,
        }
        return render(request, 'shopapp/group-list.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        url = reverse_lazy('shopapp:group-list')
        return redirect(url)


# def product_list(request: HttpRequest) -> HttpResponse:
#     products = Product.objects.all()[:10]
#     context = {
#         'products': products,
#     }
#     return render(request, 'shopapp/product-list.html', context=context)

# class ProductListView(TemplateView):
#     template_name = 'shopapp/product-list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         return context

class ProductListView(ListView):
    template_name = 'shopapp/product-list.html'
    queryset = Product.objects.filter(archived=False)[:3]
    context_object_name = 'products'


# def product_detail(request: HttpRequest, pk) -> HttpResponse:
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'product': product,
#     }
#     return render(request, 'shopapp/product-detail.html', context=context)

class ProductDetailView(DetailView):
    template_name = 'shopapp/product-detail.html'
    queryset = Product.objects.prefetch_related('images').all()
    context_object_name = 'product'


# def create_product(request: HttpRequest) -> HttpResponse:
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             Product.objects.create(**form.cleaned_data)
#             url = reverse('shopapp:product-list')
#             return redirect(url)
#
#     else:
#         form = ProductForm()
#
#     context = {
#             'form': form,
#         }
#     return render(request, 'shopapp/product_form.html', context=context)

# def create_product(request: HttpRequest) -> HttpResponse:
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse('shopapp:product-list')
#             return redirect(url)
#     else:
#         form = ProductForm()
#
#     context = {
#             'form': form,
#         }
#     return render(request, 'shopapp/product_form.html', context=context)

class ProductCreateView(UserPassesTestMixin, CreateView):

    def test_func(self):
        return self.request.user.is_superuser

    model = Product
    fields = 'name', 'description', 'price', 'preview'
    success_url = reverse_lazy('shopapp:product-list')


class ProductUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.is_superuser

    model = Product
    # fields = 'name', 'description', 'price', 'preview'
    template_name_suffix = '_update'
    form_class = ProductForm

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

    def get_success_url(self):
        return reverse(
            'shopapp:product-detail',
            kwargs={'pk': self.object.pk},
        )


class ProductDeleteView(UserPassesTestMixin, DeleteView):

    def test_func(self):
        return self.request.user.is_superuser

    model = Product
    success_url = reverse_lazy('shopapp:product-list')


class ProductArchiveView(ProductDeleteView):
    template_name_suffix = '_confirm_archive'

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archived': product.archived
            }
            for product in products
        ]

        return JsonResponse({'products': products_data})


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/order-list.html'
    model = Order
    context_object_name = 'orders'


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    template_name = 'shopapp/order-detail.html'
    model = Order
    context_object_name = 'order'


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = 'user', 'delivery_address', 'promocode'
    success_url = reverse_lazy('shopapp:order-list')
