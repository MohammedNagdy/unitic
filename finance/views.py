from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.conf import settings
from account.models import UserMembership
from .forms import GeneralEntryForm, IncomeStatementDateForm
from .models import GeneralEntry
from django.urls import reverse_lazy
import datetime # datetime lib for gettin the start and end dates
from dashboard.decorators import unanthenticated_user, user_has_membership
from django.http import JsonResponse
from django.template.loader import render_to_string
from .allAccountsFetch import performance, fetch_all



# show the entries as in the book view
def show_entries(request):
    objects = GeneralEntry.objects.all()
    context = {
        'object_list':objects
    }
    return render(request, 'finance/showentries.html', context)

# render the json response from the modal form
def create_entry(request):
    template = 'finance/createentry.html'
    data = dict()
    if request.method == 'POST':
        form = GeneralEntryForm(request.POST)
        if form.is_valid():
            # get the database model to save the input
            # data in it from the form and check the
            # validation of the input data
            obj = GeneralEntry()
            obj.user = request.user
            obj.secondary_account = form.cleaned_data.get('secondary_account')
            obj.amount = form.cleaned_data.get('amount')
            obj.date = form.cleaned_data.get('date')
            obj.percentage = form.cleaned_data.get('percentage')
            obj.recursion = form.cleaned_data.get('recursion')
            obj.date_of_payment = form.cleaned_data.get('date_of_payment')
            obj.date_of_service = form.cleaned_data.get('date_of_service')
            obj.name_of_buyer_or_seller = form.cleaned_data.get('name_of_buyer_or_seller')
            obj.paid = form.cleaned_data.get('paid')
            obj.description = form.cleaned_data.get('description')

            obj.save()
            data['form_is_valid'] = True
            # to clear out the page of the form
            objects = GeneralEntry.objects.all()
            # get the data list then post it in the view
            # of the showentries.html with the class of
            # table
            data['entry_list'] = render_to_string('finance/entry_table.html', {'object_list':objects})
        else:
            data['form_is_valid'] = False
    else:
        form = GeneralEntryForm()

    context = {
        'form':form
    }
    data['html_form'] = render_to_string(template, context, request=request)
    return JsonResponse(data)




# the show function
def income_statement(request):
    template = "finance/incomestatement.html"
    # get the the default start and
    # end dates for IS
    start_date = datetime.date(2020, 1,1)
    end_date = datetime.date.today()
    # post the start and end dates in the view
    # then fetch the data from the view
    # to fetch the entry data for each account
    form = IncomeStatementDateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

    # fetch all the accounts from the database
    params = fetch_all(request, start_date, end_date)

    # get gross profit
    gross_profit = params["sales"] - params["cost_of_sales"]

    # get total operation expenses
    operation_exp = params["sg_a"] + params["research_and_development"]
    # get operation income
    op_income = gross_profit - operation_exp

    # income before tax
    income_before = (op_income - params["int_exp"]) + params["other_income"]

    # get net income
    net_income = income_before - params["tax_exp"]

    context = params

    # to get the perfomances
    new_performances = {}
    params_performance = fetch_all(request, datetime.date(1000,1,1), datetime.date(8000,12,12))
    for param in params_performance:
        try:
            if param != "list_of_"+param:
                new_performances[(param+"_performance")] = performance(params[param], params_performance[("list_of_"+param)])
        except KeyError:
            pass
    print(new_performances)
    # get the perfomance of other accounts on the IS = income statement
    context["gross_profit_performance"] = new_performances["sales_performance"] - new_performances["cost_of_sales_performance"]

    # get total operation expenses
    context["operation_exp_performance"] = new_performances["sg_a_performance"] + new_performances["research_and_development_performance"]
    # get operation income
    context["op_income_performance"] = context["gross_profit_performance"] - context["operation_exp_performance"]

    # income before tax
    context["income_before_performance"] = (context["op_income_performance"] - new_performances["int_exp_performance"]) + new_performances["other_income_performance"]

    # get net income
    context["net_income_performance"] = context["income_before_performance"] - new_performances["tax_exp_performance"]
    # put theses performances in the context




    # get gross profit
    gross_profit_p = params["sales"] - params["cost_of_sales"]

    # get total operation expenses
    operation_exp_p = params["sg_a"] + params["research_and_development"]
    # get operation income
    op_income_p = gross_profit - operation_exp

    # income before tax
    income_before = (op_income - params["int_exp"]) + params["other_income"]

    # get net income
    net_income = income_before - params["tax_exp"]


    #add the addtional calcualtions to context
    context["gross_profit"] = gross_profit
    context["operation_exp"] = operation_exp
    context["op_income"] = op_income
    context["income_before"] = income_before
    context["net_income"] = net_income
    # form of the dates
    context["form"] = form
    # start and end dates
    # of the IS
    context["start_date"] = start_date
    context["end_date"] = end_date

    return render(request, template, context)
