from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fraud_app.urls')),
    path('api/', include('fraud_app.api_urls')),
]
