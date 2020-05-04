# this class is for loan interest and principal calculation
import datetime
import math
import decimal

class LoanCalculation:

    # time delta fn
    def timedelta(self, start, end):
      return (end-start).days/365
    # create the loan funstion quarterly

    # create the loan funstion quarterly
    def loan(self, amount, percentage, start_loan, start, end,payment_date):
      # calculation of the differenc of days between dates
      timedelta1 = self.timedelta(start_loan, start)
      timedelta2 = self.timedelta(start_loan, end)
      # get the diff between the big part and the small part
      # meaning we get the big portion of days in t_exp_2
      # then subtract t_exp_1 "the small portion of days" from
      # t_exp_2
      t_exp_start = amount * decimal.Decimal(math.pow((1+percentage),timedelta1))
      t_exp_end = amount * decimal.Decimal(math.pow((1+percentage),timedelta2))
      total = t_exp_end - t_exp_start
      # hold the total amount when the loan ends
      if end > payment_date or end == payment_date:
        new_delta = self.timedelta(start_loan, start)
        new_delta2 = self.timedelta(start_loan, payment_date)
        t_exp_start = amount * decimal.Decimal(math.pow((1+percentage),new_delta))
        t_exp_end = amount * decimal.Decimal(math.pow((1+percentage),new_delta2))
        total = ( t_exp_end - t_exp_start ) + amount
      # return zeros when the lookup window passes the loan
      # maturity date
      if start > payment_date:
        total = 0
      return round(total, 2)
