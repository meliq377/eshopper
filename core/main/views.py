from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Product, Category, Brand
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


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
        brands = Brand.objects.all()
        products = Product.objects.order_by('-id')
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
        brands = Brand.objects.all()
        products = Product.objects.filter(category__slug=slug).order_by('-id')
        products_b = Product.objects.filter(brand__slug=slug).order_by('-id')
        context = {
            'categories': categories,
            'brands': brands,
            'products': products,
            'products_b': products_b,
        }
        return render(request, self.template_name, context)
