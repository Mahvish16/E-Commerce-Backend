from django.contrib import admin
from .models import Product,Category, ProductImages,Cart,Order_item,Addresses

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order_item)
admin.site.register(Addresses)