from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, RegisterForm
from .models import Profile
from django.contrib.auth.models import User
import uuid

@login_required
def index_view(request):
    form_data = request.session.get('form_data')
    request.session.pop('form_data', None)
    return render(request, 'index.html', {'form_data': form_data})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['form_data'] = form.cleaned_data
                    return redirect('index_view')
                else:
                    messages.error(request, 'Account not activated. Please check your email.', extra_tags='red')
            else:
                messages.error(request, 'Invalid username or password.', extra_tags='red')
        else:
            messages.error(request, 'Invalid username or password.', extra_tags='red')
    else:
        form = LoginForm()

    return render(request, 'login.html', {"form": form})

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = request.POST.get('password1')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is taken.')
                return redirect('/register')

            user = form.save(commit=False)
            user.set_password(password)
            user.is_active = False  # Deactivate account till it is verified
            user.save()

            token = str(uuid.uuid4())
            profile = Profile.objects.create(user=user, auth_token=token)
            profile.save()

            send_mail_after_registration(email, token)

            messages.success(request, 'We have sent you an email to verify your account.')
            return redirect('success')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    error_message = error.split(':', 1)[-1].strip()
                    messages.error(request, error_message)
    else:
        form = RegisterForm()

    return render(request, 'register.html', {"form": form})

def send_mail_after_registration(email, token):
    subject = "Your account needs to be verified"
    message = f'Hi, paste the link to verify your account: http://127.0.0.1:8000////verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login_user')

def token_send(request):
    return render(request, 'token_send.html')

def success(request):
    return render(request, 'success.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            user = profile_obj.user
            user.is_active = True
            user.save()
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login_user')
        else:
            messages.error(request, 'Invalid token.')
            return redirect('error_page')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('error_page')

def error_page(request):
    return render(request, 'error.html')

def verification_view(request):
    return render(request, 'otp1.html')

def put_otp(request):
    return render(request, 'otp2.html')
