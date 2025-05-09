from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

#from ecomm.ec.app.views import STATUS_CHOICES
#payment
from django.utils.timezone import now
# Create your models here.
STATE_CHOICES = (
    ('Barisal', 'Barisal'),
    ('Chattogram', 'Chattogram'),
    ('Dhaka', 'Dhaka'),
    ('Khulna', 'Khulna'),
    ('Mymensingh', 'Mymensingh'),
    ('Rajshahi', 'Rajshahi'),
    ('Rangpur', 'Rangpur'),
    ('Sylhet', 'Sylhet'),
)


CATEGORY_CHOICES = (
    ('FI', 'Fiction'),
    ('NF', 'Non-Fiction'),
    ('SF', 'Science-Fiction'),
    ('HI', 'History'),
    ('FA', 'Fantasy'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default="")
    author = models.CharField(max_length=100, blank=True, null=True)
    prodapp = models.TextField(default="")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product/')
    
    # Add these new fields
    format = models.CharField(max_length=50, default='Hardcover')
    pages = models.IntegerField(default=100)
    dimensions = models.CharField(max_length=100, default='6.25 × 9.25 inches')
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=20, default='000-0000000000')
    language = models.CharField(max_length=50, default='English')

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return self.name

class Cart(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   product=models.ForeignKey(Product, on_delete=models.CASCADE) 
   quantity=models.PositiveIntegerField(default=1)

@property
def total_cost(self):
    return self.quantity * self.product.discounted_price

#payment
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)  # Bkash/Nagad/etc.
    phone_number = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id}"
    
    
#payment
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(default=now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancel', 'Cancel'),
    )
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"