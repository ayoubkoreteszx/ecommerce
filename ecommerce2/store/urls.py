from django.urls import path
from . import views


urlpatterns=[
    path("Cart/<id>",views.Cart,name="Cart"),
    path("Checkout/",views.Chechout,name="Checkout"),
    path("",views.Store,name="Store"),
    path("product_list/<id>",views.product_list,name="product_list"),
    path("update_item/",views.updateItem,name="update_item"), 
    path("process_order/",views.processOrder,name="process_order"),
    path("Home/",views.home,name="Home"),
    path("About/",views.about,name="About"),
    path("Contact/",views.contact,name="Contact"),
    path("product/<id>",views.product,name="product"),
]
