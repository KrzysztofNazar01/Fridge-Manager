from django.shortcuts import render, redirect
from ..models import Product
from ..forms import ProductForm
from django.http import HttpResponseRedirect


def product_list(request):
    products = Product.objects.all().order_by('expire_date')
    return render(request, 'product/products_list.html', {'products': products})


def product_add(request):
    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/products/add?submitted=True')
    else:
        form = ProductForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'product/product_add.html',
                  {'form': form, 'submitted': submitted})


# fridge_id comes from the url
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product/product_details.html', {'product': product})


# product_id comes from the url
def product_update(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product/product_update.html',
                  {'product': product,
                   "form": form})


# product_id comes from the url
def product_delete(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    return redirect('product_list')
