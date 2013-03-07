# Create your views here.

from django.views.generic import ListView, DetailView
from products.models import Product, ProductImage, Designer, Category

# django shortcut for passing a context to HttpResponse and 404 error
from django.shortcuts import render_to_response, get_object_or_404
import django.contrib.staticfiles
from django.http import HttpResponse, Http404

class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.all()
    template_name = 'products/index.html'
    
    # adding more context variables and selections
    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['latest_products'] = Product.objects.all().order_by("-pub_date")[:4]
        return context
        
class CategoryList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/category_list.html'
    
    def get_queryset(self):   
        category = get_object_or_404(Category, id=self.kwargs['cat'])
        return Product.objects.filter(category_id = category.id)
    
    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['cat'])
        context['categories'] = Category.objects.all()
        return context

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        product = self.get_object()
        context['image_list'] = ProductImage.objects.filter(product_id = product.id)
        context['category'] = product.category
        context['categories'] = Category.objects.all()
        context['latest_products'] = Product.objects.filter(category = product.category).exclude(id = product.id).order_by("-pub_date")[:4]
        return context

class ContactList(ListView):
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.all()
    template_name = 'products/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def index(request):
    latest_product_list = Product.objects.all().order_by('-pub_date')[:9]
    active_product_list = Product.objects.filter(is_active=1).order_by('-pub_date')[:6]
    designer_list = Designer.objects.all()
    return render_to_response('products/index.html', 
                             {'latest_product_list': latest_product_list,
                              'active_product_list': active_product_list,
                              'designer_list': designer_list,
                              'stylesheet': 'main.css'  
                             })
    
def detail404(request, product_id):
    try:
        p = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404
    return render_to_response('products/detail.html', {'product': p})


def somemethod(request, product_id):
    return HttpResponse("You're looking at product %s." % product_id)
