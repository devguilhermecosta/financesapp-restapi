from django.urls import path
from . import views

app_name = 'balance'

urlpatterns = [
    path('', views.BalanceView.as_view(), name="report"),
    path('create/', views.ReceiveView.as_view(), name="create"),
    path('list/', views.ReceiveList.as_view(), name="list"),
]
