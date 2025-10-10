from django.db import models

# Create your models here.
class CreditPrediction(models.Model):
    Age = models.IntegerField()
    Years_in_Business = models.IntegerField()
    Annual_Income = models.FloatField()
    Loan_Amount = models.FloatField()
    Outstanding_Debt = models.FloatField()
    Credit_Utilization_Rate = models.FloatField()
    Number_of_Past_Loans = models.IntegerField()
    Past_Defaults = models.IntegerField()
    Payment_History_Score = models.FloatField()
    Collateral_Value = models.FloatField()
    Business_Type = models.CharField(max_length=100)
    Region = models.CharField(max_length=100)
    Economic_Sector = models.CharField(max_length=100)
    predicted_risk = models.FloatField()
    credit_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} - Risk: {self.predicted_risk:.2f}%"
    
    

class BorrowerApplication(models.Model):
    Age = models.IntegerField()
    Years_in_Business = models.FloatField()
    Annual_Income = models.FloatField()
    Loan_Amount = models.FloatField()
    Outstanding_Debt = models.FloatField()
    Credit_Utilization_Rate = models.FloatField()
    Number_of_Past_Loans = models.IntegerField()
    Past_Defaults = models.IntegerField()
    Payment_History_Score = models.FloatField()
    Collateral_Value = models.FloatField()
    Business_Type = models.CharField(max_length=100)
    Region = models.CharField(max_length=100)
    Economic_Sector = models.CharField(max_length=100)
    predicted_risk = models.FloatField(null=True, blank=True)
    credit_score = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Borrower Application #{self.id} - {self.Business_Type} ({self.Region})"


    




