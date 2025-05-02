from django.db import models
from django.contrib.auth.models import User
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

