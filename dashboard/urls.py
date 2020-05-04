from django.urls import path
from .views import DashboardView
from .decorators import unanthenticated_user, user_has_membership

urlpatterns = [
    path('', user_has_membership(DashboardView.as_view()), name='dashboard')
]
