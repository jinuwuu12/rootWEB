from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import product_info
from inventoryflowApp.models import product_log

admin.site.register(product_info)
admin.site.register(product_log)
