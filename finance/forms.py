from django.forms import ModelForm
from django.conf import settings
from django import forms
import datetime as datetime
from .models import GeneralEntry
from .fin_accounts import FIN_CHOICES, RECURSION # choices of accounts for the user

# paid or not radio select
CHOICES = [
    ("p","paid")
]


# class of dateinput widget to post the date
# as a calender template not plain text
class DateInput(forms.DateInput):
    input_type = "date"

# create the form for entry
class GeneralEntryForm(forms.Form):
    # the fields of the form
    secondary_account = forms.ChoiceField(choices=FIN_CHOICES)
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DateInput)
    date_of_payment = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DateInput, required=False)
    date_of_service = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DateInput, required=False)

    # get the percentage field
    percentage = forms.DecimalField(max_digits=50, decimal_places=2,required=False )
    recursion = forms.ChoiceField(choices=RECURSION,required=False)

    #the rest of the fields
    amount = forms.DecimalField(max_digits=50, decimal_places=2)
    name_of_buyer_or_seller = forms.CharField(max_length=100, required=False)
    paid = forms.BooleanField(required=False)
    description = forms.CharField(max_length=1000, widget=forms.Textarea, required=False)

    # all the fields and models for the entry
    class Meta:
        model = GeneralEntry
        fields = [
            "secondary_account",
            "amount",
            "date",
            "date_of_payment",
            "date_of_service",
            "name_of_buyer_or_seller",
            "paid",
            "description"
        ]

    # checl of the data is cleaned and check if there are
    # errors iu validation
    def clean_data(self):
        cleaned_data = super().clean()
        date_of_payment = clean_data.get('date_of_payment')
        date_of_service = clean_data.get('date_of_service')

        # check if the date entered < the current date
        if date_of_payment < datetime.today() or date_of_service < datetime.today():
            raise forms.ValidationError(
                "Invalid date! It's in the past!"
            )

# form for dates range for income statement
class IncomeStatementDateForm(forms.Form):
    # get the start date
    start_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DateInput, required=True)
    # get the end date
    end_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DateInput, required=True)

    # show
    class Meta:
        fields = [
            "start_date",
            "end_date"
        ]
