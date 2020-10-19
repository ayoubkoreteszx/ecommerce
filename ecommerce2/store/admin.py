from django.contrib import admin
from .models import Order,Customer,Product,ShippingCard,OrderItem,Category,Images,Size

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
 #sets up values for how admin site lists categories
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)

 # sets up slug to be generated from category name
prepopulated_fields = {'slug' : ('name',)} 
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingCard)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Images)
admin.site.register(Size)




