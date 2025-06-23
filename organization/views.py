from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Organization
from django.utils import timezone
from .models import Event
from .forms import EventForm
from student.models import Registration
from django.contrib.auth.decorators import login_required


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event)  # Get registered students

    return render(request, "event_detail.html", {
        "event": event,
        "registrations": registrations
    })


def current_events(request):
    print("Session data:", request.session.items())
    if 'org_name' not in request.session:  # Ensure organization is logged in
        return redirect('index')
    
    org_name = request.session['org_name']  
    current_events = Event.objects.filter(organization__user__username=org_name, event_date__gt=timezone.now())



    return render(request, 'current_events.html', {'events': current_events})

def org_login_view(request):
    error = None  # Initialize error variable

    if request.method == 'POST':
        username = request.POST.get('school_name')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is an organization
            if Organization.objects.filter(user=user).exists():
                login(request, user)  # Log in the user
                request.session['org_name'] = username  # Set session
                return redirect('dashboard')  # Redirect to dashboard
            else:
                error = "You are not an organization."  # Store error message
        else:
            error = "Invalid username or password."  # Store error message

    organizations = Organization.objects.all()
    return render(request, 'org_login.html', {'organizations': organizations, 'error': error})



def logout_view(request):
    logout(request)
    request.session.flush()  # Clear session
    return redirect('index')  # Redirect back to login page
@login_required
def dashboard_view(request):
    
    
    org_name = request.session.get('org_name', 'Organization')
    return render(request, 'dashboard.html', {'org_name': org_name})



def create_event(request):
    # Get the logged-in organization directly
    try:
        org = Organization.objects.get(user=request.user)
    except Organization.DoesNotExist:
        return redirect('index')  # Redirect normal users

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organization = org  # Assign the organization to the event
            event.save()
            return redirect('dashboard')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})

def close_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure only the event's organization can close registration
    if event.organization.user != request.user:
        messages.error(request, "You don't have permission to do that.")
        return redirect('event_detail', event_id=event_id)

    # Close registration
    event.registration_open = False
    event.save()

    messages.success(request, "Registration has been closed.")
    return redirect('event_detail', event_id=event_id)