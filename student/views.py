from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .forms import RegisterForm, LoginForm
from .models import Profile, Registration
from django.core.mail import send_mail
import uuid
from organization.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError


@login_required
def events(request):
    student = request.user  # Get logged-in student
    events = Event.objects.filter(registration_open=True)  # ✅ Only open events

    for event in events:
        event.is_registered = Registration.objects.filter(student=student, event=event).exists()

    return render(request, "events.html", {"events": events})

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    student = request.user

    # Register the student if they aren't already signed up
    if not Registration.objects.filter(student=student, event=event).exists():
        Registration.objects.create(student=student, event=event)

    return redirect("events") 
# Home

def index(request):
    return render(request, 'index.html', {'title': 'Home Page'})

# Register

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.username = str(uuid.uuid4())[:8]  
            user.is_active = False  
            user.save()

            # Save g_number in Profile
            try:
                Profile.objects.create(
                    user=user,
                    g_number=form.cleaned_data['g_number']
                )
            except IntegrityError: # already created an account 
                messages.error(request, "An account with this user already exists")
                user.delete()
                return redirect('register')
            # Send verification email...
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'form': form})


# Email Verification View
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        profile = Profile.objects.get(user=user)
        profile.verified = True
        profile.save()

        return redirect('login')
    else:
        return render(request, 'invalid_token.html')


# Login View
def login_view(request):
    error = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                error = "Email does not exist."
                return render(request, 'login.html', {'form': form, 'error': error})

            user = authenticate(request, email=email, password=password)

            if user is None:
                print("Authentication failed for:", email)
                error = "Incorrect email or password."
                return render(request, 'login.html', {'form': form, 'error': error})

            print("Authentication successful:", user)

            login(request, user)
            print("User logged in successfully:", request.user)

            profile = Profile.objects.get(user=user)
            if profile.verified:
                return redirect('events')
            else:
                error = "Please verify your email first."

    return render(request, 'login.html', {'form': LoginForm(), 'error': error})
def logout_view(request):
    
    logout(request)  # Logs out the user
    request.session.flush()
    return redirect("index")

def resend_verification(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)

            if profile.verified:
                messages.error(request, "Your email is already verified.")
                return redirect("login")

            # Generate a new verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Send Verification Email
            verification_link = request.build_absolute_uri(
                reverse("verify_email", args=[uid, token])
            )
            send_mail(
                "Resend Verification Email",
                f"Click the link to verify your account: {verification_link}",
                "noreply@example.com",
                [user.email],
            )

            messages.success(request, "Verification email sent successfully!")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")

    return render(request, "resend_verification.html")