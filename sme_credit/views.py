from django.shortcuts import render

from .forms import PredictionForm
from .models import CreditPrediction
import joblib
import numpy as np
import pandas as pd

model = joblib.load("credit_risk_pipeline.pkl")
model_features = joblib.load("model_features.pkl")


def predict_credit_score(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

           
            data['Business_Type'] = str(data['Business_Type'])
            data['Region'] = str(data['Region'])
            data['Economic_Sector'] = str(data['Economic_Sector'])

            numeric_fields = [
                'Age', 'Years_in_Business', 'Annual_Income', 'Loan_Amount',
                'Outstanding_Debt', 'Credit_Utilization_Rate',
                'Number_of_Past_Loans', 'Past_Defaults', 'Payment_History_Score',
                'Collateral_Value'
            ]
            for field in numeric_fields:
                data[field] = float(data[field])

         
            import pandas as pd
            df_input = pd.DataFrame([data])

        

            # Make prediction
            prediction = model.predict(df_input)[0]
            prob = model.predict_proba(df_input)[0][1] * 100  # percentage

             # Interpret prediction
            if prediction == 1:
                result = "High Risk (Likely to Default)"
            else:
                result = "Low Risk (Likely to Repay)"

            return render(request, 'result.html', {
                'prediction': result,
                'probability': round(prob, 2),
            })

    else:
        form = PredictionForm()

    return render(request, 'predict_form.html', {'form': form})




