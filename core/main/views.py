from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Product, Category, Brand


class IndexListView(ListView):
    template_name = 'main/index.html'

    def get(self, request):
        categories = Category.objects.filter(parent=None)
        context = {
            'categories': categories,
        }
        return render(request, self.template_name, context)
