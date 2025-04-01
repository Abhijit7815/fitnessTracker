from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('login_view/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workouts/', views.workout_view, name='workout_view'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('workout/<int:workout_id>/', views.workout_detail_view, name='workout_detail'),
    path('diet-plan/', views.diet_plan_view, name='calculate_diet_plan'),
    path('calorie-calc/', views.calculate_calories, name='calculate_calories'),
    path('calculate_bodyfat/', views.calculate_bodyfat, name='calculate_bodyfat'),

]
