from django.db import models

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

# used by django-cart classes
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

saved_file.connect(generate_aliases_global)


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __unicode__(self):
        return self.name
    
class Designer(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
       
class Product(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField('date published')
    designer = models.ForeignKey(Designer)
    is_active = models.BooleanField('Active', default = False)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ['name']
    
class Variant(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    uid = models.PositiveIntegerField()
    is_active = models.BooleanField('Active', default = False)
    
    def __unicode__(self):
        return self.name
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='product_images')
    
    def url(self):
        return self.image.url
        
class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name='creation date')
    checked_out = models.BooleanField(default=False, verbose_name= 'checked out')

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='cart')
    quantity = models.PositiveIntegerField(verbose_name='quantity')
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='unit price')
    
    # product as generic relation
    content_type = models.ForeignKey(ContentType, related_name='contents')
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)



