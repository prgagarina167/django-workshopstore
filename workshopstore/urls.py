from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from products.views import ProductList, ProductDetail, CategoryList, ContactList, CartList, AddtoCartList, RemoveFromCartList

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', ProductList.as_view(), name='index'),
    # url(r'^workshopstore/', include('workshopstore.foo.urls')),
    # url(r'^products/$', 'products.views.index'),
    url(r'^products/$', ProductList.as_view()),
    url(r'^products/(?P<cat>\d+)/$', CategoryList.as_view()),
    url(r'^product/(?P<pk>\d+)/$', ProductDetail.as_view()),
    url(r'^contact/$', ContactList.as_view()),
    url(r'^cart/$', CartList.as_view()),
    url(r'^cart/add/(?P<product_id>\d+)/$', AddtoCartList.as_view()),
    url(r'^cart/remove/(?P<product_id>\d+)/$', RemoveFromCartList.as_view()),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# ... the rest of your URLconf goes here ...

urlpatterns += staticfiles_urlpatterns()