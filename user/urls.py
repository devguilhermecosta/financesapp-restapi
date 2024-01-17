from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('<int:id>/', views.UserDetailAPIView.as_view(), name='detail'),
    path('list/', views.UserListAPIView.as_view(), name='list'),
]
