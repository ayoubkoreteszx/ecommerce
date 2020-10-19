from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(null=True,help_text='A valid email address,please.') 
    objects = models.Manager()

    def __str__(self):
        return  self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
    help_text='Unique value for product page URL, created from name.')
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255,
    help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
    help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager() 

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name 
      
    def get_absolute_url(self):
        return reverse('store_category', args=(self.slug,))  

class Size(models.Model):
    nameSize = models.CharField(max_length=50)
    objects = models.Manager()

    def __str__(self):
        return self.nameSize 

class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.DecimalField(max_digits=7,decimal_places=2)
    description=models.TextField(blank=True,null=True)
    image=models.ImageField(blank=True,null=True,default="images/default.jpg")
    size=models.ManyToManyField(Size)
    digital=models.BooleanField(default=False,null=True,blank=True)
    categories = models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True, null=True) 
    objects = models.Manager() 

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/images/default.jpg"

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_orderd=models.DateField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    transaction_id=models.CharField(max_length=200,null=True)
    objects = models.Manager() 

    def __str__(self):
        return str(self.pk)
    
    @property
    def shipping(self):
        shipping=False
        orderItems=self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital==False:
                shipping=True
        return shipping

    @property
    def get_cart_total(self):
       orderitems=self.orderitem_set.all()
       total=sum([item.get_total for item in orderitems ])
       return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    size=models.CharField(max_length=200,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateField(auto_now_add=True)
    objects = models.Manager() 

    def __str__(self):
         return self.product.name

    @property     
    def get_total(self):
        total=self.product.price*self.quantity
        return total    
     
    
 
class ShippingCard(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateField(auto_now_add=True,null=True,blank=True)
    delivrable=models.BooleanField(null=True,blank=False)
    notDelivrable=models.BooleanField(null=True,blank=True)
    
    def __str__(self):
        return  self.address


class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    title=models.CharField(max_length=200,null=True,blank=True)
    image=models.ImageField(blank=True,null=True)

    def __str__(self):
        return str(self.title) if self.title else 'image'

     
       
