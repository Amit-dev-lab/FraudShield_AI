from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.key[:8]}..."

class FraudTransaction(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('pending', 'Pending'),
    ]
    
    RECOMMENDATION_CHOICES = [
        ('approve', 'Approve'),
        ('decline', 'Decline'),
        ('review', 'Review'),
    ]
    
    # Input data
    trans_date_trans_time = models.DateTimeField()
    category = models.CharField(max_length=50)
    amount_inr = models.FloatField()
    sender_city = models.CharField(max_length=100)
    receiver_city = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    has_previous_transaction = models.BooleanField(default=False)
    previous_transaction_date = models.DateTimeField(null=True, blank=True)
    
    # Calculated features
    distance_km = models.FloatField()
    city_pop = models.IntegerField()
    age = models.IntegerField()
    hour = models.IntegerField()
    weekday = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()
    is_night = models.BooleanField()
    secs_since_last = models.FloatField(default=0)
    
    # Legacy fields for compatibility
    currency = models.CharField(max_length=10, default='INR')
    location = models.CharField(max_length=200, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    merchant_id = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Results
    risk_score = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATION_CHOICES)
    fraud_probability = models.FloatField()
    confidence_score = models.FloatField()
    processing_time = models.FloatField()  # milliseconds
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Transaction {self.id} - {self.status}"
