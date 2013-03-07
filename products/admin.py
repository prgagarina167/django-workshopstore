from django.contrib import admin
from products.models import Product, Variant, Designer, Category, ProductImage

class VariantInline(admin.StackedInline):
    model = Variant
    extra = 1

class ImageInline(admin.TabularInline):
    model = ProductImage
   
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category','name', 'description', 'price','designer','is_active']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    list_display = ('name','designer','is_active')
    search_fields = ['name']
    list_filter = ('pub_date',)
    ordering = ('name',)
    inlines = [VariantInline, ImageInline]
    


admin.site.register(Product, ProductAdmin)
admin.site.register(Designer)
admin.site.register(Category)