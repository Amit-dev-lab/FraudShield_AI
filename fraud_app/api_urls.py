from django.urls import path
from .api_views import FraudPredictionAPIView

urlpatterns = [
    path('predict/', FraudPredictionAPIView.as_view(), name='api_predict'),
]
