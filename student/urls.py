from django.contrib.auth.decorators import login_required

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path("events/", views.events, name="events"),
    path("events/register/<int:event_id>/", views.register_event, name="register_event"),
    path('logout/', views.logout_view, name='logout'),
    path("resend-verification/", views.resend_verification, name="resend_verification"),
]
