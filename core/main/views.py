import requests
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.http import JsonResponse
import json
from django.core import serializers
from django.http import HttpResponse


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "main/register.html", {'form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'main/login.html', context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


class IndexListView(ListView):
    template_name = 'main/index.html'

    def get(self, request):
        categories = Category.objects.filter(parent=None)
        products = Product.objects.order_by('-id')
        brands = Brand.objects.annotate(cnt=Count('products')).filter(cnt__gt=0)
        context = {
            'categories': categories,
            'brands': brands,
            'products': products,
        }
        return render(request, self.template_name, context)


class CategoryListView(ListView):
    template_name = 'main/category.html'

    def get(self, request, slug):
        categories = Category.objects.filter(parent=None)
        brands = Brand.objects.annotate(cnt=Count('products')).all()
        products = Product.objects.filter(category__slug=slug).order_by('-id')
        products_b = Product.objects.filter(brand__slug=slug).order_by('-id')
        context = {
            'categories': categories,
            'brands': brands,
            'products': products,
            'products_b': products_b,
        }
        return render(request, self.template_name, context)


def add_to_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if OrderProduct.objects.filter(user=request.user.id, product_id=prod_id):
                    return JsonResponse({'status': 'Product Already in Cart'})
                else:
                    prod_qty = Product.objects.get(pk=prod_id).quantity

                    if product_check.quantity >= prod_qty:
                        OrderProduct.objects.create(user_id=request.user.id, product_id=prod_id, price=Product.objects.get(pk=prod_id).price, quantity=prod_qty)
                        return JsonResponse({'status': 'Product added successfully'})
                    else:
                        return JsonResponse({'status': 'Only ' + str(product_check.quantity) + 'quantity available'})
            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': 'Login to Continue'})
    return redirect('/')

def cartview(request):
    cart = OrderProduct.objects.filter(user=request.user)
    context = {'cart': cart}
    return render(request, 'main/cart.html', context)