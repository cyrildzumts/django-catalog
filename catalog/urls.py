from django.conf.urls import url
from catalog import views

app_name = 'catalog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^livraison/$', views.livraison, name='livraison'),
    url(r'^flyer/$', views.flyer, name='flyer'),
    #url(r'^faq/$', views.faq_view, name='faq'),
    url(r'^search/$', views.search_view, name='search'),
    #url(r'^(?P<category_slug>[-\w]+)/$', views.show_category,
    #    name='catalog_category'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.CategoryView.as_view(),
        name='catalog_category'),
    # url(r'^product/(?P<product_slug>[-\w]+)/$', views.show_product,
    #    name='product_details'),
    url(r'^product/(?P<slug>[-\w]+)/$', views.ProductDetailView.as_view(),
        name='product_details'),
]
