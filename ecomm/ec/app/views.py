from django.db.models import Count
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . models import Product,Cart,Product
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from .models import Customer
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! You have registered successfully.')
        else:
            messages.warning(request, 'Invalid input data. Please try again.')
        return render(request, 'app/customerregistration.html', locals())
            
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcode=zipcode
            )
            reg.save()
            messages.success(request, "Congratulations! Profile saved successfully.")
        else:
            messages.warning(request, "Invalid input data.")
        return render(request, 'app/profile.html', locals())
#only fetch customer profile where customer was login
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

class updateAddress(View):
    def get(self, request, pk):
        add = get_object_or_404(Customer, pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', {'form': form})

    def post(self, request, pk):
        add = get_object_or_404(Customer, pk=pk)
        form = CustomerProfileForm(request.POST, instance=add)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Profile updated successfully.")
        else:
            messages.warning(request, "Invalid input data.")
        return redirect("address")

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())

@csrf_exempt
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.filter(product=prod_id, user=request.user).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()

            # Recalculate cart totals
            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40

            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item not found'}, status=404)