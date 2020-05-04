"""oneplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from account import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from dashboard.decorators import unanthenticated_user, not_auth


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', not_auth(views.HomeView.as_view()), name="home"),
    path('register/', not_auth(views.RegisterView.as_view()), name="register"),
    path('login/', not_auth(auth_views.LoginView.as_view(template_name="login.html")), name="login"),
    # check plans view
    path('check/', not_auth(views.check_plans), name="check"),
    # the rest of the main views
    path('logout/', unanthenticated_user(auth_views.LogoutView.as_view(template_name="logout.html")), name="logout"),
    path('memberships-plans/', not_auth(views.PlansView.as_view()), name="plans"),

    path('memberships/', unanthenticated_user(views.MembershipsView.as_view()), name="memberships"),
    # all the add delete ur;s for the product in the cart
    path('add/<slug:slug>/', unanthenticated_user(views.add_to_cart), name="add-to-cart"),
    path('remove/<slug:slug>/', unanthenticated_user(views.delete_from_cart), name="delete-item"),
    path('order-details/', unanthenticated_user(views.order_details), name="order-details"),
    path('delete/<slug:slug>',unanthenticated_user(views.delete_from_memberships), name="delete-membership"),
    # all the payment processing URLs
    path('checkout/<slug:ref_code>/', unanthenticated_user(views.CheckOut.as_view()), name="checkout"),
    path('process-<slug:token>/', unanthenticated_user(views.update_transaction_records), name="payment"),
    path('add-membership/<slug:ref_code>/', unanthenticated_user(views.add_membership), name="add-membership"),
    path('payment-success/', unanthenticated_user(views.Success.as_view()), name="success"),
    # dashboard urls
    path('dashboard/', include('dashboard.urls')),
    # finance app urls
    path('finance/', include('finance.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
