# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render

from product.forms import ProductForm
from product.models import Product


def product_view(request):
    products = Product.objects.filter(user=request.user)
    # import ipdb; ipdb.set_trace()

    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            product.user = request.user
            product.save()
            return HttpResponseRedirect('/product')
    else:
        product_form = ProductForm()

    context = {'product_form': product_form, 'products': products}
    return render(request, 'product.html', context)
