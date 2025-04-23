from django.db.models import Count
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from . models import Product
from .forms import CustomerRegistrationForm

def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html',locals())
class CategoryTitle(View):
    def get(self, request, val):
        # Get products matching the selected category
        product = Product.objects.filter(title=val)
        # Get unique titles of products in the same category
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())
class ProductDetail(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',locals())
    

class CustomerRegistationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())