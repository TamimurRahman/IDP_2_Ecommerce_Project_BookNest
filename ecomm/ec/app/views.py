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
from django.db import models
from django.contrib.auth.models import User
#for pamentgateway implementation
from .models import Payment, Cart, OrderPlaced
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Payment,Wishlist



def home(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())


def about(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())


def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())

class CategoryView(View):
    def get(self, request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html',locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        # Get products matching the selected category
        product = Product.objects.filter(title=val)
        # Get unique titles of products in the same category
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/category.html", locals())
    
class ProductDetail(View):
    def get(self, request,pk):
        totalitem = 0
        wishlist=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',locals())
    

class CustomerRegistationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishlist=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! You have registered successfully.')
        else:
            messages.warning(request, 'Invalid input data. Please try again.')
        return render(request, 'app/customerregistration.html', locals())

@method_decorator(login_required,name='dispatch')            
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

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        add = get_object_or_404(Customer, pk=pk)
        totalitem = 0
        wishlist=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
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

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
    totalamount = amount + 40
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishlist=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40 if cart_items.exists() else 0
        return render(request, 'app/checkout.html', locals())

@login_required
def orders(request):
    totalitem = 0
    wishlist=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())
    
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
@csrf_exempt
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.filter(product=prod_id, user=request.user).first()

        if cart_item:
            cart_item.quantity -= 1
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
@csrf_exempt
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(product=prod_id, user=request.user).first()

        if cart_item:
            cart_item.delete()

        # Recalculate totals after deletion
        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart)
        shipping = 40 if amount > 0 else 0
        totalamount = amount + shipping

        data = {
            'amount': amount,
            'shipping': shipping,
            'totalamount': totalamount,
            'cart_empty': not cart.exists()
        }
        return JsonResponse(data)
    



#here apply ssclecommerz payment gateway
@login_required
def payment_confirm(request):
    if request.method == "POST":
        method = request.POST.get("payment_method")
        phone = request.POST.get("phone_number")
        tx_id = request.POST.get("transaction_id")
        custid = request.POST.get("custid")
        total = request.POST.get("totamount")

        # Save payment
        payment = Payment.objects.create(
            user=request.user,
            amount=total,
            payment_method=method,
            phone_number=phone,
            transaction_id=tx_id,
            paid=True
        )

        # Place orders
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            OrderPlaced.objects.create(
                user=request.user,
                customer_id=custid,
                product=item.product,
                quantity=item.quantity,
                payment=payment
            )
        cart_items.delete()
        return redirect("orders")



def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.create(user=user, product=product)
        return JsonResponse({'message': 'Wishlist Added Successfully'})

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist Removed Successfully',
        }
        return JsonResponse(data)

def add_to_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        user = request.user

        # Check if item already in cart
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('showcart')  # Replace with your cart page name

def search(request):
    query = request.GET.get('search')
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()

    product = Product.objects.filter(title__icontains=query)

    return render(request, "app/search.html", locals())
