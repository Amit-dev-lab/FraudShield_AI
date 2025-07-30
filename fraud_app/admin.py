from django.contrib import admin
from .models import APIKey, FraudTransaction

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'key', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'key']

@admin.register(FraudTransaction)
class FraudTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'status', 'fraud_probability', 'amount_inr', 'created_at']
    list_filter = ['status', 'recommendation', 'category', 'created_at']
    search_fields = ['sender_city', 'receiver_city', 'created_by__username']
    readonly_fields = ['created_at']
