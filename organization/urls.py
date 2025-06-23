from django.urls import path
from .views import org_login_view, logout_view, dashboard_view, current_events, event_detail,create_event, close_registration

urlpatterns = [
    path('', org_login_view, name='org_login'),
    path('logout/', logout_view, name='org_logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('current-events/', current_events, name='current_events'),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path('create_event/', create_event, name='create_event'),
    path("events/<int:event_id>/close/", close_registration, name="close_registration"),

]


