from rest_framework import serializers

class FraudPredictionSerializer(serializers.Serializer):
    trans_date_trans_time = serializers.DateTimeField()
    category = serializers.CharField(max_length=50)
    amount_inr = serializers.FloatField()
    sender_city = serializers.CharField(max_length=100)
    receiver_city = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    has_previous_transaction = serializers.BooleanField(default=False)
    previous_transaction_date = serializers.DateTimeField(required=False, allow_null=True)

class FraudPredictionResponseSerializer(serializers.Serializer):
    is_fraud = serializers.BooleanField()
    fraud_probability = serializers.FloatField()
    risk_score = serializers.FloatField()
    confidence_score = serializers.FloatField()
    status = serializers.CharField()
    recommendation = serializers.CharField()
    processing_time = serializers.FloatField()
    transaction_id = serializers.IntegerField()
