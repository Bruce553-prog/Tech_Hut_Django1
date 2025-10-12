from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import PredictionForm
from .models import CreditPrediction
from .models import BorrowerApplication
from django.contrib import messages
from . borrowerform import BorrowerForm
from django.contrib.auth.decorators import login_required


import joblib
import numpy as np
import pandas as pd

model = joblib.load("credit_risk_pipeline.joblib")
model_features = joblib.load("credit_risk_pipeline.joblib")



def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # or borrower form, if that’s their dashboard
    return render(request, 'home.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        login(request, user)
        messages.success(request, f"Welcome {username}, your account has been created!")
        return redirect('dashboard')

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}!")
            return redirect('dashboard')  # redirect to a dashboard page
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
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





@login_required
def borrower_form_view(request):
    if request.method == 'POST':
        form = BorrowerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            BorrowerApplication.objects.create(
                Age=data['Age'],
                Years_in_Business=data['Years_in_Business'],
                Annual_Income=data['Annual_Income'],
                Loan_Amount=data['Loan_Amount'],
                Outstanding_Debt=data['Outstanding_Debt'],
                Credit_Utilization_Rate=data['Credit_Utilization_Rate'],
                Number_of_Past_Loans=data['Number_of_Past_Loans'],
                Past_Defaults=data['Past_Defaults'],
                Payment_History_Score=data['Payment_History_Score'],
                Collateral_Value=data['Collateral_Value'],
                Business_Type=data['Business_Type'],
                Region=data['Region'],
                Economic_Sector=data['Economic_Sector']
            )
            
            return render(request, 'borrower_success.html')
    else:
        form = BorrowerForm()
        

    return render(request, 'borrower_form.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

