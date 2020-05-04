from .loan_calculation import LoanCalculation # a custom class to calucate the interest expense of loans
from .models import GeneralEntry # the model we fetch the from

# calculating performance indicator
def performance(value, lst):
    try:
        return round((((value-min(lst))/(max(lst)-min(lst)))*100),2)
    except Exception as e:
        print("we got this error in the performance function at allAccountsFetch module... ", e)
        return 0

# calucating percentages for sales, cost and cash
def percentages(old, new):
    try:
        return round((((new - old)/old) * 100 ),2)
    except ZeroDivisionError :
        return round((((new - old)/1) * 100 ),2)

# fetch all the accounts from the database
def fetch_all(request, start_date, end_date ):
    # get revenues & sales
    rev = GeneralEntry.objects.filter(user=request.user, secondary_account="revenue", date__range=[start_date, end_date])
    reev = [i.amount for i in rev]
    summation_rev = sum(reev)
    # get the costs of the sales
    cost_of_sales =  GeneralEntry.objects.filter(user=request.user, secondary_account="cost_of_sales", date__range=[start_date, end_date])
    costs_of_sales = [i.amount for i in cost_of_sales]
    summation_cost_of_sales = sum(costs_of_sales)
    # get gross profit
    gross_profit = summation_rev - summation_cost_of_sales

    # get salaries general & adminstrative expenses
    sg_a = GeneralEntry.objects.filter(user=request.user, secondary_account="employee_expense", date__range=[start_date, end_date])
    sg_as = [i.amount for i in sg_a]
    summation_sg_a = sum(sg_as)

    # get R&D Expenses
    research_and_development = GeneralEntry.objects.filter(user=request.user, secondary_account="research_and_development", date__range=[start_date, end_date])
    research_and_developments = [i.amount for i in research_and_development]
    summation_research = sum(research_and_developments)
    # get total operation expenses
    operation_exp = summation_sg_a + summation_research
    # get operation income
    op_income = gross_profit - operation_exp

    # get interest expenses
    """
    #############################################################################################
    GOT THE INTEREST PAYMENT PROBLEM FIXED THROUGH LOAN CALCULATION CLASS IN loan_calculation.py
    #############################################################################################
    """
    # there is a mispelling in percentage as precentage
    calc = LoanCalculation()
    #calc.loan(i.amount, i.percentage/100, i.date, start_date, end_date, i.date_of_payment)
    int_exp = GeneralEntry.objects.filter(user=request.user, secondary_account="loan")
    ints_exp = [calc.loan(i.amount, float(i.precentage/100), i.date, start_date, end_date, i.date_of_payment) for i in int_exp]
    # get the expense of the perido
    summation_int_exp = sum(ints_exp)
    # get other incomes or expenses from asset sales
    asset_sale = GeneralEntry.objects.filter(user=request.user, secondary_account="asset_sale", date__range=[start_date, end_date])
    # get the summation of each then total
    # get the total other inceom or expenses
    # from asset sales for now
    assets_sale = [i.amount for i in asset_sale]
    summation_asset_sale = sum(assets_sale)

    # cash investment
    cash_inv = GeneralEntry.objects.filter(user=request.user, secondary_account="investment", date__range=[start_date, end_date])
    cash_innv = [i.amount for i in cash_inv]
    summation_cash_inv = sum(cash_innv)


    # income before tax
    income_before = (op_income - summation_int_exp) + summation_asset_sale + summation_cash_inv
    # get tax expenses
    tax_exp = GeneralEntry.objects.filter(user=request.user, secondary_account="taxes", date__range=[start_date, end_date])
    taxes_exp = [i.amount for i in tax_exp]
    summation_tax_exp = sum(taxes_exp)

    # get net income
    net_income = income_before - summation_tax_exp


    params = {
            "list_of_sales": reev,
            "sales":summation_rev,
            "list_of_cost_of_sales": costs_of_sales,
            "cost_of_sales":summation_cost_of_sales,
            "list_of_research_and_development": research_and_developments,
            #"gross_profit":gross_profit,
            "research_and_development":summation_research,
            "list_of_sg_a": sg_as,
            "sg_a":summation_sg_a,

            #"operation_exp":operation_exp,
            #"op_income":op_income,
            "list_of_int_exp": ints_exp,
            "int_exp":summation_int_exp,
            "list_of_other_income":assets_sale,
            "other_income": summation_asset_sale,
            #"income_before": income_before,
            "list_of_tax_exp": taxes_exp,
            "tax_exp": summation_tax_exp,
            #"net_income": net_income
    }

    return params
