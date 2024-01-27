from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, SquatCustomizationForm, BicepCurlCustomizationForm
from django.urls import reverse  # Add this import
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SquatCustomization, BicepCurlCustomization




def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard'))  # Update the URL name
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')  



def logout_view(request):
    logout(request)
    return redirect('login')

def user_profile_view(request):
    return render(request, 'accounts/user_profile.html')

def customize_routine_view(request):
    if request.method == 'POST':
        squat_form = SquatCustomizationForm(request.POST, prefix='squat')
        bicep_curl_form = BicepCurlCustomizationForm(request.POST, prefix='bicep_curl')

        if squat_form.is_valid() and bicep_curl_form.is_valid():
            # Get the form data
            rep_count_squat = squat_form.cleaned_data['rep_count_squat']
            time_limit_squat = squat_form.cleaned_data['time_limit_squat']

            rep_count_bicep_curl = bicep_curl_form.cleaned_data['rep_count_bicep_curl']
            time_limit_bicep_curl = bicep_curl_form.cleaned_data['time_limit_bicep_curl']

            # Save the form data to the database
            squat_customization = SquatCustomization(user=request.user, rep_count=rep_count_squat, time_limit=time_limit_squat)
            squat_customization.save()

            bicep_curl_customization = BicepCurlCustomization(user=request.user, rep_count=rep_count_bicep_curl, time_limit=time_limit_bicep_curl)
            bicep_curl_customization.save()

            # Redirect the user to a relevant page, for example, the dashboard
            return redirect('dashboard')
    else:
        squat_form = SquatCustomizationForm(prefix='squat')
        bicep_curl_form = BicepCurlCustomizationForm(prefix='bicep_curl')

    return render(request, 'accounts/customize_routine.html', {'squat_form': squat_form, 'bicep_curl_form': bicep_curl_form})
def shared_with_you_view(request):
    return render(request, 'accounts/shared_with_you.html')

