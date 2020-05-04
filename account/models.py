from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# memberships for each app depending on the database space
MEMBERSHIPS = (
    ("small","سركات صغيرة"),
    ("midsize", ""),
    ("corp","")
)



# costum model field for lists
import ast

class ListField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

# memberships model
class Memberships(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=50)
    # membership_type = models.CharField(
    #     choices=MEMBERSHIPS,
    #     max_length=30
    # )
    price = models.IntegerField()
    stripe_plan_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# connecting memberships to users
class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    stripe_customer_id = models.CharField(max_length=50)
    membership = ListField(blank=True)

    def __str__(self):
        return self.user.username

# post user_membership stripe id or create one
def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)

    user_membership, created = UserMembership.objects.get_or_create(user=instance)

    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == "":
        new_customer_id = stripe.Customer.create(email=instance.email)
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.save()

post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)




# model to check if the user has that subscription and it
# gathers both models
class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=50)
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.user_membership.user.username




# models for the cart and the checkout
class OrderItem(models.Model):
    product = models.ForeignKey(Memberships, models.SET_NULL, null=True)
    # product = models.CharField(max_length=100, null=True)

    is_ordered = models.BooleanField(default=False)
    date_added = models.DateField(auto_now=True)
    date_ordered = models.DateField(null=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    ref_code = models.CharField(max_length=39)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    # payment_details = mddels.ForeignKey(Payment)
    date_ordered = models.DateField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return f"{self.owner} has {self.items}"

# transaction model to record the payment
class Transaction(models.Model):
    profile = models.ForeignKey(UserMembership, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_length=100, decimal_places=2, max_digits=50)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']
