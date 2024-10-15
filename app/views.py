from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import CustomUser
import logging
import random
from django.core.mail import send_mail
from django.db import IntegrityError

logger = logging.getLogger(__name__)
User = get_user_model()

def generate_otp():
    return str(random.randint(100000, 999999))  # Generate a 6-digit OTP as a string

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')

        # Check password confirmation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        # Check for existing username or email
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'register.html')

        # Create the user instance
        user = CustomUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
        )
        user.set_password(password)

        try:
            # Save the user to get user ID
            user.save()

            # Store user data in session
            request.session['temp_user'] = {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'date_of_birth': date_of_birth,
                'password': password,
            }

            # Generate the OTP
            otp_code = generate_otp()
            request.session['otp_code'] = otp_code  # Store OTP in session

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is: {otp_code}',
                'your-email@example.com',  # Replace with your sending email
                [email],
                fail_silently=False,
            )

            messages.success(request, "Registration successful! Check your email for the OTP.")
            return redirect('verify_otp', user.id)  # Redirect to OTP verification page with user ID

        except IntegrityError as e:
            # Log the specific error for debugging
            logger.error(f"IntegrityError: {e}")  # Log the error to help debug
            messages.error(request, "An error occurred during user creation. Please try again.")
            return render(request, 'register.html')

        except Exception as e:
            # Catch all other exceptions and log them
            logger.error(f"Unexpected error: {e}")  # Log the unexpected error
            messages.error(request, "An unexpected error occurred. Please try again.")
            return render(request, 'register.html')

    return render(request, 'register.html')


def verify_otp_view(request, user_id):  # Add 'user_id' parameter here
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_code = request.session.get('otp_code')

        # Check if OTP exists in session
        if not otp_code:
            messages.error(request, "OTP code is missing. Please request a new OTP.")
            return redirect('resend_otp')

        # Verify the OTP entered matches the one in the session
        if entered_otp == str(otp_code):
            user = CustomUser.objects.get(id=user_id)

            # Check if the user exists and is not already verified
            if user:
                try:
                    # Mark the user as verified
                    user.is_verified = True
                    user.save()  # Save the changes to the user

                    # Clear session data upon successful verification
                    del request.session['temp_user']
                    del request.session['otp_code']

                    messages.success(request, "OTP verification successful! You can now log in.")
                    return redirect('login')

                except IntegrityError as e:
                    logger.error(f"IntegrityError: {e}")
                    messages.error(request, "An error occurred during user creation. Please try again.")
                    return redirect('register')
            else:
                messages.error(request, "User not found. Please try registering again.")
                return redirect('register')

        else:
            messages.error(request, "Invalid OTP! Please try again.")
            return redirect('verify_otp', user_id=user_id)

    # Render the OTP verification page
    return render(request, 'verify_otp.html', {'user_id': user_id})




def resend_otp_view(request):
    user_data = request.session.get('temp_user')
    if user_data:
        user_email = user_data['email']
        otp_code = generate_otp()
        request.session['otp_code'] = otp_code  # Store new OTP in session

        # Send new OTP via email
        send_mail(
            'Your OTP Code',
            f'Your new OTP code is: {otp_code}',
            'your-email@example.com',  # Replace with your sending email
            [user_email],
            fail_silently=False,
        )

        messages.success(request, "A new OTP has been sent to your email.")
    else:
        messages.error(request, "User data not found in session!")

    return redirect('verify_otp')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')  # Redirect to the dashboard after logging in
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)  # Log out the user
    messages.success(request, "Logout successful!")
    return redirect('login')


@login_required
def index_view(request):
    return render(request, 'index.html')  # Render the dashboard template
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')  # Render the dashboard template

