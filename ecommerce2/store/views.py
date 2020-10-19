from django.shortcuts import render,get_object_or_404,redirect
from .models  import Customer,Order ,OrderItem ,Product,User,Category,ShippingCard,Images
from  django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext 
from django.http import JsonResponse
from  . utils import cookieCart,cartData,guestOrder
from django.db.models.query import QuerySet
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import get_template 
from django.db.models import Count
from .form import ContactForm
from django.core.exceptions import  MultipleObjectsReturned


# Create your views here.
def Chechout( request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,"store/Checkout.html",context)

def Store(request):
    data=cartData(request)
    cartItems=data['cartItems']
    products=Product.objects.all()
    context={"products":products}
    return render(request,'store/Store.html',context)
    
def Cart(request,id):
    data=cartData(request)
    cartItems=data['cartItems']
    items=data['items']
    print(items)
    #size=request.POST.get('size')
    #print("hhh",size)
    for item in items:
        print(item)
    order=data['order']
    context={"items":items,"order":order}
    return render(request,'store/Cart.html',context)

def show_category(request, category_slug):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description 
    return render(request,'store/Main.html/',locals())

def product_list(request,id):
    products = Product.objects.filter(categories__pk=id)
    context = {
      'products': products,
    }
    return render(request,'store/product_list.html',context)


def updateItem(request):
    data=json.loads(request.body)
    print(data)
    productId=data['productId']
    action=data['action']
    size=data['size']
    print(productId)
    print(action)
    print(size)
    customer=request.user.customer
    product=Product.objects.get(id=productId) 
    print(product)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    #try:
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    orderItem.size=size
    if action == "add":
          orderItem.quantity=(orderItem.quantity+1)
    
    elif action == "remove":
           orderItem.quantity=(orderItem.quantity-1)
           

    orderItem.save()
    if orderItem.quantity<=0:
           orderItem.delete()
           
    #except OrderItem.MultipleObjectsReturned:
      # orderItem=OrderItem.objects.filter(order=order,product=product) 
      # print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
      # for item in orderItem:

        # orderItem.quantity=0
        # orderItem.size="XL"
       
       #if action == "add":
       # orderItem.quantity=(orderItem.quantity+1)
       # orderItem.size=size
       #elif action == "remove":
        #orderItem.quantity=(orderItem.quantity-1)
       #orderItem.save()
       #if orderItem.quantity<=0:
       #orderItem.delete()
    
    return JsonResponse('Item was added',safe=False)
    
@csrf_exempt
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
    else :
        customer,order=guestOrder(request,data)

    total=float(data['form']['total'])
    order.transaction_id=transaction_id

    if total==order.get_cart_total:
        order.complete=True
    order.save()

    if order.shipping==True:
            ShippingCard.objects.create(
                customer=customer,
                order=order,
                address=data['shipping'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                delivrable=data['shipping']['delivrable'],
                notDelivrable=data['shipping']['notDelivrable'],
            )   
    return JsonResponse('Payment complete',safe=False)

def home(request):
        context={}
        return render(request,'store/Home.html',context)

def contact(request):
    Contact_Form=ContactForm
    if request.method=='POST':
        form=Contact_Form(data=request.POST)

        if form.is_valid():
            template=get_template("store/contact_form.txt")
            content={
                'contact_name':request.POST.get('contact_name'),
                'contact_email':request.POST.get('contact_email'),
                'contact_content':request.POST.get('content'),
            }
            content=template.render(content)
            email=EmailMessage(
                "new contact form email",
                content,
                'luxe et broderie'+'',
                ['idrissiashop@gmail.com'],
                headers={'contact_email': 'contact_email'},         
            )
            email.send()
            return redirect('/')
    return render(request,'store/Contact.html',{'form':Contact_Form})

def about(request):
        return render(request,'store/About.html',{})

def product(request,id):
    p = get_object_or_404(Product, id=id)
    img=p.images_set.all()
    data=cartData(request)
    cartItems=data['cartItems']
    size=request.POST.get("size")
    #print(size)
    return render(request,'store/Product.html',{'product':p,'img':img,'size':size})
 
