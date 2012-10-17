from django.db import models

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

