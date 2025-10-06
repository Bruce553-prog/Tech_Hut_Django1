from django.shortcuts import render

from .forms import PredictionForm
from .models import CreditPrediction
import joblib
import numpy as np
import pandas as pd

model = joblib.load("credit_risk_pipeline.joblib")
model_features = joblib.load("model_features.joblib")


def predict_credit_score(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            df = pd.DataFrame([data])

            # One-hot encode like during training
            df_encoded = pd.get_dummies(df)
            missing_cols = set(model_features) - set(df_encoded.columns)
            for col in missing_cols:
                df_encoded[col] = 0
            df_encoded = df_encoded[model_features]

            prediction = model.predict_proba(df_encoded)[0][1]
            predicted_risk = prediction * 100
            credit_score = 100 - predicted_risk  # Simplified logic

            CreditPrediction.objects.create(
                **data,
                predicted_risk=predicted_risk,
                credit_score=credit_score
            )

            context = {
                'form': form,
                'predicted_risk': f"{predicted_risk:.2f}",
                'credit_score': f"{credit_score:.2f}"
            }
            return render(request, 'result.html', context)
    else:
        form = PredictionForm()

    return render(request, 'predict_form.html', {'form': form})




