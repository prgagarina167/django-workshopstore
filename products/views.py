# Create your views here.

from django.views.generic import ListView, DetailView
from products.models import Product, ProductImage, Designer, Category
from cart import Cart, ItemAlreadyExists, ItemDoesNotExist

# django shortcut for passing a context to HttpResponse and 404 error
from django.shortcuts import render_to_response, get_object_or_404
import django.contrib.staticfiles
from django.http import HttpResponse, Http404

# form
from products.forms import ContactForm
from django.views.generic.edit import FormView

#class ContactView(FormView):
#    template_name = 'products/contact.html'
#    form_class = ContactForm
#    success_url = '/products/'
#
#    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
#        form.send_email()
#        return super(ContactView, self).form_valid(form)

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
    queryset = Product.objects.all()
    template_name = 'products/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CartList(ListView):
    #import pdb; pdb.set_trace()
    template_name = 'products/cart.html'
    
    def get_queryset(self):   
        return Cart(self.request)
    
    def get_context_data(self, **kwargs):
        context = super(CartList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cart'] = Cart(self.request)
        #import pdb; pdb.set_trace()
        context['cart_total'] = Cart(self.request).summary
        return context
        
class AddtoCartList(ListView):
    template_name = 'products/cart.html' 
    
    def get_queryset(self):  
        return Cart(self.request)
    
    def get_context_data(self, **kwargs):
        context = super(AddtoCartList, self).get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs['product_id'])
        Cart(self.request).add(product, product.price, 1)
        context['categories'] = Category.objects.all()
        context['cart'] = Cart(self.request)
        context['cart_total'] = Cart(self.request).summary
        return context
        
class RemoveFromCartList(ListView):
    template_name = 'products/cart.html' 
    
    def get_queryset(self):  
        return Cart(self.request)
    
    def get_context_data(self, **kwargs):
        context = super(RemoveFromCartList, self).get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs['product_id'])
        Cart(self.request).remove(product)
        context['categories'] = Category.objects.all()
        context['cart'] = Cart(self.request)
        context['cart_total'] = Cart(self.request).summary
        return context

class WritemeView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)

# django-cart views
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    return render_to_response('products/cart.html', cart.add(product, product.price, quantity=1))

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)

def get_cart(request):
    return render_to_response('products/cart.html', dict(cart=Cart(request)))

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
