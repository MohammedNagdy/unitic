from django.urls import path
from .views import DashboardView, get_data
from .decorators import unanthenticated_user, user_has_membership

urlpatterns = [
    path('', user_has_membership(DashboardView.as_view()), name='dashboard'),
    path('api/line-data', user_has_membership(get_data), name='line-data'),
]
