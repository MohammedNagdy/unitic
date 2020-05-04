from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse # returnung str into http HttpResponse
from django.conf import settings
from django.db.models.query import EmptyQuerySet # to check if the query is empty
from django.contrib import messages
from django.views import View
from .forms import RegisterForm
from .models import Memberships, OrderItem, Cart, UserMembership, Transaction
from django.views.generic import ListView
from django.urls import reverse # reverse to the previous url
import uuid # this is for the ref_code generation
import stripe # for payments
import datetime # for recording the date of the transactions of the payment
from dashboard.decorators import unanthenticated_user

stripe.api_key = settings.STRIPE_SECRET_KEY





# get the user or return nothing
def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(UserMembership, user=request.user)
    order = Cart.objects.filter(owner=user_profile.user, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

# check if the user has plans to redirect to dashboard or
# memberships page once logging in
def check_plans(request):
    # get plans from the user
    user_profile = get_object_or_404(UserMembership, user=request.user)
    print(isinstance((UserMembership.objects.filter(user=request.user, membership__exact='')), EmptyQuerySet))
    print(user_profile.membership is '')
    if user_profile.membership is '':
        return redirect(reverse('memberships'))
    else:
        return redirect(reverse('dashboard'))

# Create your views here.
class HomeView(View):
    template = 'index.html'
    # get home template
    def get(self, request):
        return render(request, self.template)


# register view
class RegisterView(View):
    template = 'register.html'
    # get register template form and show the form
    def get(self, request):
        form = RegisterForm()

        context = {
            'form' : form,
        }

        return render(request, self.template, context)


    # take in the data from the user
    def post(self, request):
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()

            return redirect('login')
        else:
            form = RegisterForm()

        context = {
            'form' : form,
        }

        return render(request, self.template, context)


# plans view for outsiders
class PlansView(ListView):
    model = Memberships
    template_name = "plans.html"


# memberships list view
class MembershipsView(View):
    model = Memberships.objects.all()
    cart_user = Cart.objects.all()
    template = 'memberships_list.html'

    def get(self, request):

        # check if there are products in the user membership model
        # already so you can delete it later
        # get the user
        # item = get_object_or_404(UserMembership, user=request.user, membership__icontains=product)
        # get all the memberships list
        p = Memberships.objects.values_list("name")
        # iterate over the memberships list
        # to find the match between the memberships and the
        # the user memebership.membership
        mr = None
        for i in p:
            # filter user to find memberships and check if they're equal
            if UserMembership.objects.filter(user=request.user, membership__icontains=str(i).strip("[('.,')]")):
                mr = str(i).strip("[('.,')])")
                break
                # context = {"cart":self.cart_user,"object_list":self.model, "membership":mr }
            else:
                mr = False
        context = {"membership":mr, "cart":self.cart_user,"object_list":self.model }

        return render(request, self.template, context)




# class AddProduct(View):
    # add to cart function
def add_to_cart(request, slug):
    # for ref code of the pusrchase
    id = uuid.uuid1()

    # get the user profile
    user_profile = get_object_or_404(UserMembership, user=request.user)
    # print(user_profile)

    # filter product by slug
    product = get_object_or_404(Memberships, slug=slug)

    # check if the user has the product
    if product == UserMembership.objects.filter(membership__contains=product):
        messages.info(request, "أنت تمتلك المنتج")


    # create order item or the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)

    # add items to the cart
    user_order, status = Cart.objects.get_or_create(owner=user_profile.user, is_ordered=False  )

    # add the items
    user_order.items.add(order_item)

    # Generate reference code
    if status:
        user_order.ref_code = id.int
        user_order.save()



    return redirect(reverse('memberships'))


def delete_from_cart(request, slug):
    # filter to get the product
    product = get_object_or_404(Memberships, slug=slug)
    # we have to pull the product from OrderItem model because it has
    # the relation with cart it's not Memberships --> Cart
    # it's Memberships --> OrderItem --> Cart
    order = get_object_or_404(OrderItem, product=product)
    # filter in the cart to remove the product
    item_to_delete = Cart.objects.filter(items=order)
    # check if the product exits in the cart
    if item_to_delete.exists():
        # if it does delete
        item_to_delete[0].delete()
        # notify the user
        messages.info(request, "Item has been deleted")
    return redirect(reverse('memberships'))


def order_details(request, **kwargs):
    # show all th eproducts ordered
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'cart.html', context)


# delete from  user memberships in the memberships_list view
def delete_from_memberships(request, slug):
    # filter to get the product
    product = get_object_or_404(Memberships, slug=slug)
    # get the item from  user membership
    item = get_object_or_404(UserMembership, user=request.user, membership__icontains=product)
    # turn the memebership list into a list and
    # store it in cache
    memberships_list = list(item.membership.strip("[]").split(","))

    # print(memberships_list)
    membersheepo_listo = [] # empty list to store non-deleted items
    # iterate to find all the unchosen products
    for i in memberships_list:
        if not str(product) in i:
            print(i)
            membersheepo_listo.append(i)
    # update the membership field with all the unchosen products
    item.membership = membersheepo_listo
    item.save()

    return redirect('/memberships/')

# add the memebership to the user
def add_membership(request, ref_code):
    # get items in cart
    user_order = get_object_or_404(Cart, ref_code=ref_code)

    user_profile = get_object_or_404(UserMembership, user=request.user)
    # getting the list of all orders in the cart
    order = [o for o in user_order.items.all()]
    usermembersheepo, _ = UserMembership.objects.get_or_create(user=request.user)

    # iterate over all orders in cart
    lst = []
    for i in order:
        # add the order from the cart to the user membership model
        # get the membership that is the same from orders in the cart
        membersheepo, _ = Memberships.objects.get_or_create(name=i.product.name)
        # add each order in the user membership model
        lst.append(membersheepo)
        # save each order in memberships un usermembership model
    usermembersheepo.membership = lst
    # print(usermembersheepo.membership)
    usermembersheepo.save()
    return redirect('/dashboard/')


# check out view
class CheckOut(View):
    # template for the checkout
    template = 'payment.html'

    # showing the orders and getting the stripe publishable_key
    def get(self, request, ref_code):
        # get the orders in the cart
        existing_order = get_user_pending_order(request)
        publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        # context to put it in views
        context = {
            'order': existing_order,
            'STRIPE_PUBLISHABLE_KEY': publishable_key,
            'ref_code': ref_code,
        }
        return render(request, self.template, context)

    # doing a post request for stripe payment
    def post(self, request, **kwargs):
        # get the orders in the cart
        existing_order = get_user_pending_order(request)
        publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        # context to put it in views
        context = {
            'order': existing_order,
            'STRIPE_PUBLISHABLE_KEY': publishable_key
        }
        if request.method == 'POST':
            # try except block for payment errors
            try:
                # grap the stripe token from the javascript form
                token = request.POST("stripeToken")
                # create the charge for Customer
                charge = stripe.Charge.create(
                    amount = self.existing_order.get_cart_total(),
                    currency = 'egp',
                    description = 'plan charge',
                    source = token,

                )
                return redirect(reverse('update-payment',
                        kwargs={
                            'token' : token,
                        }
                    )
                )

            # exceptions for the errors
            except stripe.CardError as e:
                messages.info(request, "Your card has been declined!")

        return render(request, self.template, context)

# updating transaction records
def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    # get all the orders that being purchased
    order_items = order_to_purchase.items.all()

    # updating the orders data
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # get the user
    user_profile = get_object_or_404(UserMembership, user=request.user.user)

    # add the products to user profile
    order_products = [item.product for item in order_items]
    user_profile.membership.add(order_products)
    user_profile.save()


    # updating the trasaction or recording it
    transaction = Transaction(
        profile = request.user.profile,
        token = token,
        order_id = order_to_purchase.id,
        amount = order_to_purchase.get_cart_total(),
        success = True,

    )
    transaction.save()

    # send an email ------ to do
    # send a message to the Customer
    messages.info(request, "Your payment has been successfully processed!")
    return redirect(reverse("dashboard"))


# views for the sucess of the payment
class Success(View):
    template = "success_payment.html"
    def get(self, request):
        return render(request, self.template)
