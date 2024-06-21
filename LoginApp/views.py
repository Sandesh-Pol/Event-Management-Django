from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, RegisterForm,OTPVerificationForm ,PasswordResetRequestForm, SetNewPasswordForm
from .models import Profile
from event_card.views import base_view
from django.contrib.auth.models import User
import uuid
from .models import OTP
import random

#authonticatin using email varifiction

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
                    return redirect('base_view')
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


# password reset 

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_via_email(user, otp):
    subject = "Your OTP for Password Reset"
    message = f"Your OTP for password reset is {otp}"
    from_email = 'your_email@example.com'
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email)

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                OTP.objects.update_or_create(user=user, defaults={'otp': otp})
                send_otp_via_email(user, otp)
                request.session['user_id'] = user.id
                return redirect('verify_otp')
            except User.DoesNotExist:
                messages.error(request, 'No user with this email found.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'otp1.html', {'form': form})

# myapp/views.py

def verify_otp(request):
    if request.method == 'POST':
        otp1 = request.POST.get('otp1').strip()
        otp2 = request.POST.get('otp2').strip()
        otp3 = request.POST.get('otp3').strip()
        otp4 = request.POST.get('otp4').strip()
        otp = f"{otp1}{otp2}{otp3}{otp4}"

        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_otp = OTP.objects.get(user=user)
                if user_otp.otp == otp:
                    return redirect('set_new_password')
                else:
                    messages.error(request, 'Invalid or expired OTP.')
            except (User.DoesNotExist, OTP.DoesNotExist):
                messages.error(request, 'Invalid OTP.')
    return render(request, 'otp2.html')


def set_new_password(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password successfully reset.')
                    return redirect('login_user')
                except User.DoesNotExist:
                    messages.error(request, 'User not found.')
    else:
        form = SetNewPasswordForm()
    return render(request, 'set_new_password.html', {'form': form})
