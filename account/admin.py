# Register your models here.
from django.contrib import admin
from .models import Memberships, UserMembership, Subscription, OrderItem, Cart
#
admin.site.register(Memberships)
admin.site.register(UserMembership)
admin.site.register(Subscription)
admin.site.register(OrderItem)
admin.site.register(Cart)
