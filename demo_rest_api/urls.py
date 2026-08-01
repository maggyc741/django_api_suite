from django.urls import path
from . import views 

from .views import DemoRestApiItem

urlpatterns = [
    path('', views.DemoRestApi.as_view(), name='demo-rest-index'),
    path('index/', views.DemoRestApi.as_view(), name='demo-rest-index'),

    path('<str:id>/', DemoRestApiItem.as_view(), name='demo-rest-api-item'),

]
