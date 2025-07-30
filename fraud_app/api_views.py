from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FraudPredictionSerializer, FraudPredictionResponseSerializer
from .ml_utils import predict_fraud
from .models import FraudTransaction
import time



class FraudPredictionAPIView(APIView):
    """API endpoint for fraud prediction"""
    
    def post(self, request):
        serializer = FraudPredictionSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                start_time = time.time()
                
                # Get prediction
                result = predict_fraud(serializer.validated_data)
                
                processing_time = (time.time() - start_time) * 1000
                result['processing_time'] = processing_time
                
                # Save transaction to database
                transaction = FraudTransaction.objects.create(
                    trans_date_trans_time=serializer.validated_data['trans_date_trans_time'],
                    category=serializer.validated_data['category'],
                    amount_inr=serializer.validated_data['amount_inr'],
                    sender_city=serializer.validated_data['sender_city'],
                    receiver_city=serializer.validated_data['receiver_city'],
                    date_of_birth=serializer.validated_data['date_of_birth'],
                    has_previous_transaction=serializer.validated_data['has_previous_transaction'],
                    previous_transaction_date=serializer.validated_data.get('previous_transaction_date'),
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
                
                response_data = {
                    'is_fraud': result['is_fraud'],
                    'fraud_probability': result['fraud_probability'],
                    'risk_score': result['risk_score'],
                    'confidence_score': result['confidence_score'],
                    'status': result['status'],
                    'recommendation': result['recommendation'],
                    'processing_time': result['processing_time'],
                    'transaction_id': transaction.id
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response(
                    {'error': f'Prediction error: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
