# custom decorators
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from account.models import UserMembership, Memberships

# checking authentication user
def unanthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        # send user home if not authenticated
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        # send user to the page if he's logged in
        else:
            return redirect(reverse("login"))
    return wrapper_func

# check if the user is not authenticated
def not_auth(view_func):
    def wrapper_func(request, *args, **kwargs):
        # check if the user is not authenticated
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('dashboard'))

    return wrapper_func

# checking if users have memberships
def user_has_membership(view_func):

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            # grap the user memberships_list
            # get plans from the user
            user_profile = get_object_or_404(UserMembership, user=request.user)
            # check if the user has memberships if
            # he doesn't it will redirect the user to
            # memberships to buy one
            if user_profile.membership is '' or user_profile.membership == '[]':
                return redirect(reverse('memberships'))
            else:
                return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))
    return wrapper_func
