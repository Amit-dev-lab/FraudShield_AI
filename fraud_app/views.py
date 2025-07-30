from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, FraudCheckForm
from .models import APIKey, FraudTransaction
from .ml_utils import predict_fraud
import time

def home(request):
    """Home page view"""
    return render(request, 'fraud_app/home.html')

def signup(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create API key for the user
            APIKey.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully! Your API key has been generated.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def manual_check(request):
    """Manual fraud check form view"""
    if request.method == 'POST':
        form = FraudCheckForm(request.POST)
        if form.is_valid():
            try:
                start_time = time.time()
                
                # Get prediction
                result = predict_fraud(form.cleaned_data)
                
                processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                result['processing_time'] = processing_time
                
                # Save transaction to database
                transaction = FraudTransaction.objects.create(
                    trans_date_trans_time=form.cleaned_data['trans_date_trans_time'],
                    category=form.cleaned_data['category'],
                    amount_inr=form.cleaned_data['amount_inr'],
                    sender_city=form.cleaned_data['sender_city'],
                    receiver_city=form.cleaned_data['receiver_city'],
                    date_of_birth=form.cleaned_data['date_of_birth'],
                    has_previous_transaction=form.cleaned_data['has_previous_transaction'],
                    previous_transaction_date=form.cleaned_data.get('previous_transaction_date'),
                    distance_km=result['features']['distance_km'],
                    city_pop=result['features']['city_pop'],
                    age=result['features']['age'],
                    hour=result['features']['hour'],
                    weekday=result['features']['weekday'],
                    day=result['features']['day'],
                    month=result['features']['month'],
                    is_night=result['features']['is_night'],
                    secs_since_last=result['features']['secs_since_last'],
                    risk_score=result['risk_score'],
                    status=result['status'],
                    recommendation=result['recommendation'],
                    fraud_probability=result['fraud_probability'],
                    confidence_score=result['confidence_score'],
                    processing_time=result['processing_time'],
                    created_by=request.user
                )
                
                return render(request, 'fraud_app/result.html', {
                    'result': result,
                    'transaction': transaction,
                    'form_data': form.cleaned_data
                })
                
            except Exception as e:
                messages.error(request, f'Error processing transaction: {str(e)}')
                
    else:
        form = FraudCheckForm()
    
    return render(request, 'fraud_app/manual_check.html', {'form': form})

@login_required
def api_key_view(request):
    """Display user's API key"""
    try:
        api_key = APIKey.objects.get(user=request.user)
    except APIKey.DoesNotExist:
        api_key = APIKey.objects.create(user=request.user)
    
    return render(request, 'fraud_app/api_key.html', {'api_key': api_key})

@login_required
def transaction_history(request):
    """Display user's transaction history"""
    transactions = FraudTransaction.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'fraud_app/history.html', {'transactions': transactions})
