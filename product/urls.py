from product.views import product_view
from django.conf.urls import url


urlpatterns = [
    url(r'^$', product_view, name='product_view'),
]
