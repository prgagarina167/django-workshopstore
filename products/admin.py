from django.contrib import admin

from products.models import Product
from products.models import Designer
from products.models import Category
from products.models import Variant

class VariantInline(admin.StackedInline):
   model = Variant
   extra = 1
   
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category','name', 'description','designer','is_active']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    list_display = ('name','designer','is_active')
    search_fields = ['name']
    list_filter = ('pub_date',)
    ordering = ('name',)
    inlines = [VariantInline]
    


admin.site.register(Product, ProductAdmin)
admin.site.register(Designer)
admin.site.register(Category)