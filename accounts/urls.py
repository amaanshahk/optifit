# accounts/urls.py
from django.urls import path
from .views import login_view, signup_view, dashboard_view, logout_view, user_profile_view, customize_routine_view, shared_with_you_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),  # Define the dashboard URL
    path('logout/', logout_view, name='logout'),  # Add this line for logout
    path('user-profile/', user_profile_view, name='user_profile'),
    path('customize-routine/', customize_routine_view, name='customize_routine'),
    path('shared-with-you/', shared_with_you_view, name='shared_with_you'),

]
