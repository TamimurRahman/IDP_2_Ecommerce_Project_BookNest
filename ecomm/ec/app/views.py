from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from . models import Product

def home(request):
    return render(request, 'app/home.html')

class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        return render(request, 'app/category.html',locals())
    
