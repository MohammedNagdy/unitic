from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.conf import settings
from account.models import UserMembership, Memberships
from finance.models import GeneralEntry
import datetime # to check dates for fetch data
from finance.loan_calculation import LoanCalculation # to do interest payment calculation
from finance.allAccountsFetch import *

# Create your views here.
# the dashboard views for the user
class DashboardView(View):
    template = "dashboard/dashboard.html"

    # get the dashboard elemeents
    def get(self, request):
        # set the start date start - 7
        end_date = datetime.date.today()
        delta = datetime.timedelta(7)
        start_date = end_date - delta
        # get last weeks results
        end_date_0 = start_date
        start_date_0 = end_date_0 - delta

        # get the weekly performance of the business

        # the total sales of this week
        rev = GeneralEntry.objects.filter(user=request.user, secondary_account="revenue", date__range=[start_date, end_date])
        reev = [i.amount for i in rev] # to use it for graphing
        total_rev = sum(reev)
        # total sales last week
        rev_0 = GeneralEntry.objects.filter(user=request.user, secondary_account="revenue", date__range=[start_date_0, end_date_0])
        total_rev_0 = sum([i.amount for i in rev])
        # the percentage difference
        rev_percentage = percentages(total_rev_0, total_rev)

        """
        get the total costs to show in the first bar
        """

        # the total costs this week
        # cost of sales + sg_a + research and development + interest
        cost_of_sales =  GeneralEntry.objects.filter(user=request.user, secondary_account="cost_of_sales", date__range=[start_date, end_date])
        total_cost_of_sales = sum([i.amount for i in cost_of_sales])
        # sg_a
        sg_a = GeneralEntry.objects.filter(user=request.user, secondary_account="employee_expense", date__range=[start_date, end_date])
        total_sg_a = sum([i.amount for i in sg_a])
        # get R&D Expenses
        research_and_development = GeneralEntry.objects.filter(user=request.user, secondary_account="research_and_development", date__range=[start_date, end_date])
        total_research = sum([i.amount for i in research_and_development])
        # there is a mispelling in percentage as precentage
        calc = LoanCalculation()
        #calc.loan(i.amount, i.percentage/100, i.date, start_date, end_date, i.date_of_payment)
        int_exp = GeneralEntry.objects.filter(user=request.user, secondary_account="loan")
        # print([float(i.precentage) for i in int_exp])
        total_int_exp = sum([calc.loan(i.amount, float(i.precentage/100), i.date, start_date, end_date, i.date_of_payment) for i in int_exp])

        # the total cost
        total_cost = total_cost_of_sales + total_sg_a + total_research + total_int_exp

        # total costs last week
        cost_of_sales_0 =  GeneralEntry.objects.filter(user=request.user, secondary_account="cost_of_sales", date__range=[start_date_0, end_date_0])
        total_cost_of_sales_0 = sum([i.amount for i in cost_of_sales_0])
        # sg_a
        sg_a_0 = GeneralEntry.objects.filter(user=request.user, secondary_account="employee_expense", date__range=[start_date_0, end_date_0])
        total_sg_a_0 = sum([i.amount for i in sg_a_0])
        # get R&D Expenses
        research_and_development_0 = GeneralEntry.objects.filter(user=request.user, secondary_account="research_and_development", date__range=[start_date_0, end_date_0])
        total_research_0 = sum([i.amount for i in research_and_development_0])
        # there is a mispelling in percentage as precentage
        calc = LoanCalculation()
        #calc.loan(i.amount, i.percentage/100, i.date, start_date_0, end_date_0, i.date_of_payment)
        int_exp_0 = GeneralEntry.objects.filter(user=request.user, secondary_account="loan")
        # print([float(i.precentage) for i in int_exp])
        total_int_exp_0 = sum([calc.loan(i.amount, float(i.precentage/100), i.date, start_date_0, end_date_0, i.date_of_payment) for i in int_exp_0])

        # the total cost
        total_cost_0 = total_cost_of_sales_0 + total_sg_a_0 + total_research_0 + total_int_exp_0

        # get the percentage of total costs
        costs_percentage = percentages(total_cost_0, total_cost)


        # inventory for this week
        inv =  GeneralEntry.objects.filter(user=request.user, secondary_account="inventory", date__range=[start_date, end_date])
        innv = [i.amount for i in inv] # to use it for grapging
        total_inv = sum(innv)
        # invetory last week
        inv_0 =  GeneralEntry.objects.filter(user=request.user, secondary_account="inventory", date__range=[start_date_0, end_date_0])
        total_inv_0 = sum([i.amount for i in inv_0])
        # get inv percentage
        inv_percentage = percentages(total_inv_0, total_inv)


        # performance indicator for sales
        lst = [i.amount for i in rev]
        performance_ = performance(total_rev, lst)
        lst_0 = [i.amount for i in rev_0]
        performance_0 = performance(total_rev_0, lst_0)
        performance_percentage = percentages(performance_0, performance_)


        """
        get the data for the charts
        """
        print(reev)
        print(innv)



        context = {
            "sales": total_rev,
            "sales_percentage": rev_percentage,
            "costs": total_cost,
            "costs_percentage": costs_percentage,
            "inv": total_inv,
            "inv_percentage": inv_percentage,
            "performance": performance_,
            "performance_percentage": performance_percentage

        }


        return render(request, self.template, context)
