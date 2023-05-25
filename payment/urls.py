from django.urls import path
from . import views
urlpatterns = [    
    path('pay/<int:id>/', views.Payment.as_view(), name="pay"),    
]