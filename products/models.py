from django.db import models

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

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



