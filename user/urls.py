from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('list/', views.UserListAPIView.as_view(), name='list'),
]
