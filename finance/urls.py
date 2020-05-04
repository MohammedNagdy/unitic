from django.urls import path
from .views import (income_statement,
                    create_entry,
                    show_entries)
from django.contrib.auth.decorators import login_required
from dashboard.decorators import user_has_membership


urlpatterns = [
    path('entries/', user_has_membership(show_entries), name="entries"),
    path('entries/general-entry/', user_has_membership(create_entry), name='general-entry'),
    path('income-statement/', user_has_membership(income_statement), name="income-statement"),
    # path("income-statement/", login_required(incomestatementview), name='income-statement')
]
