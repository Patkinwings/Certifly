# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('payment/', views.payment_view, name='payment'),
    path('payment/success/', views.payment_success_view, name='payment_success'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('test/<int:test_id>/', views.TestView.as_view(), name='take_test'),
    path('create_question/<int:test_id>/', views.create_question_view, name='create_question'),
    path('upload_question_image/<int:question_id>/', views.upload_question_image, name='upload_question_image'),
    path('execute-command/', views.execute_command, name='execute_command'),
]