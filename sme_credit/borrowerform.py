from django import forms
from .models import BorrowerApplication
class BorrowerForm(forms.Form):
    Age=forms.IntegerField(min_value=18, max_value=100)
    Years_in_Business = forms.IntegerField(min_value=0)
    Annual_Income = forms.FloatField(min_value=0)
    Loan_Amount = forms.FloatField(min_value=0)
    Outstanding_Debt = forms.FloatField(min_value=0)
    Credit_Utilization_Rate = forms.FloatField(min_value=0, max_value=1)
    Number_of_Past_Loans = forms.IntegerField(min_value=0)
    Past_Defaults = forms.IntegerField(min_value=0)
    Payment_History_Score = forms.FloatField(min_value=0, max_value=1000)
    Collateral_Value = forms.FloatField(min_value=0)
    Business_Type = forms.ChoiceField(choices=[
        ('Retail','Retail'),('Manufacturing','Manufacturing'),
        ('Agriculture','Agriculture'),('Technology','Technology'),
        ('Services','Services')
    ])
    Region = forms.ChoiceField(choices=[
        ('Kenya','Kenya'),('Nigeria','Nigeria'),
        ('South Africa','South Africa'),('Ghana','Ghana'),
        ('Uganda','Uganda')
    ])
    Economic_Sector = forms.ChoiceField(choices=[
        ('SME','SME'),('Corporate','Corporate'),('Individual','Individual')
    ])


    

      








