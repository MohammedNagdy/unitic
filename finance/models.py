from django.db import models
from account.models import UserMembership
from django.conf import settings

"""
this model takes any business transaction puts it
into the accounting books using the accounting
equation and other methods

All the inflows of a business is through
1- Revenue/Sales Accrued or not .... Paid or not
2- Funding/Investments/Loans  Assets or Cash
All the outflows of a business is through
1- Expenses  Accrued or not ... Paid or not---->Monthly/Quarterly/Semi-Annually/Annual
2- Taxes Paid or not---->Monthly/Quarterly/Semi-Annually/Annual
3- Capital Expenditure
 -----------------------------------------------------
| ACCOUNTING EQUATION                                 |
|        ASSETS = LIABILITIES + SHAREHOLDER'S EQUITY  |
 -----------------------------------------------------
THE METHOD USED:
        Inputs(
          secondary_account,
          amount,
          date,
          date_of_payment=null,
          date_of_service=null,
          name_of_buyer_or_seller,
          paid=True or False,
          description=null,

"""
class GeneralEntry(models.Model):
    # user = models.OneToOneField(UserMembership, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    # create all the inputs of the general entry
    secondary_account = models.CharField(max_length=100)
    amount = models.DecimalField( max_length=100, decimal_places=2, max_digits=50)
    precentage = models.DecimalField(max_length=10, decimal_places=2, max_digits=10, default="0.00", null=True)
    recursion = models.CharField(max_length=100, blank=True ,null=True)
    date = models.DateField(auto_now_add=False, auto_now=False)
    date_of_payment = models.DateField( auto_now=False, blank=True, null=True)
    date_of_service = models.DateField( auto_now=False, blank=True, null=True)
    name_of_buyer_or_seller = models.CharField(null=True, max_length=100, blank=True)
    paid = models.BooleanField(default=True)
    description = models.CharField(max_length=500, blank=True)

    def get_total_range_statements(self):
        return sum([transaction.amount for transaction in self.entries.all()])

    # order entries by date
    class Meta:
        ordering = ['-date']
