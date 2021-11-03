from django.contrib import admin
from .models import BronxMember, Transaction, StockItem

# Register your models here.
admin.site.register(BronxMember)
admin.site.register(Transaction)
admin.site.register(StockItem)
