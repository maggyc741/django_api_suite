from django.urls import path
from . import views 

urlpatterns = [
    path('index/', views.DemoRestApi.as_view(), name='demo-rest-index'),
    
]
