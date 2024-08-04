# core/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('payment/', views.payment_view, name='payment'),
    path('payment/success/', views.payment_success_view, name='payment_success'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('test/<int:test_id>/', views.take_test, name='take_test'),
    path('create_question/<int:test_id>/', views.create_question_view, name='create_question'),
    path('admin/core/question/<int:question_id>/upload-image/', views.upload_question_image, name='admin_upload_question_image'),
    path('execute-command/', views.execute_command, name='execute_command'),
    path('start-new-session/', views.start_new_session, name='start_new_session'),
    path('handle-command/', views.handle_command, name='handle_command'),
    
    # Password reset URLs
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # New URLs for one-question-at-a-time functionality
    path('test/<int:test_id>/question/<int:question_index>/', views.get_question, name='get_question'),
    path('test/<int:test_id>/submit_answer/', views.submit_answer, name='submit_answer'),
    path('test/<int:test_id>/finish/', views.finish_test, name='finish_test'),
]