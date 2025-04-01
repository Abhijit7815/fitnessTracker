from django.shortcuts import render, redirect
from django.http import HttpResponse
import math
from .models import *

def index(request):
    return render(request, 'index.html')
def contact_us(request):
    return render(request,'contact_us.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password and not Person.objects.filter(email=email).exists():
            user = Person(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password  # Store password as plain text (not recommended for production)
            )
            user.save()
            return redirect('login_view')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = Person.objects.get(email=email)
            if password == user.password:  # Plain text password comparison
                # Simulating the login process by setting the user in session
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                # Password did not match
                return render(request, 'login.html', {'error': 'Invalid password'})
        except Person.DoesNotExist:
            # No user found with this email
            return render(request, 'login.html', {'error': 'Invalid email'})
    
    return render(request, 'login.html')

def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_view')
    
    user = Person.objects.get(id=user_id)
    if user.weight and user.height:
        height_m = user.height / 100  # Convert height to meters if height is in cm
        bmi = user.weight / (height_m ** 2)
        if bmi<18.5:
            bmi_message ="You are underweight."
        elif bmi<25:
            bmi_message ="Your bmi is normal."
        elif bmi<30:
            bmi_message ="You are overweight."
        else:
            bmi_message ="You are obese."
        
    else:
        bmi = 'N/A'
        bmi_message = "Height and weight data are needed to calculate BMI."

    context = {
        'user': user,
        'bmi': bmi,
        'bmi_message': bmi_message,
    }
    
    return render(request, 'home.html', context)


def workout_view(request):
    exercises = Workout.objects.all()
    user_id = request.session.get('user_id')
    user = Person.objects.get(id=user_id)

    context1={
    'user':user,
    }
    context2 = {
        'exercises': exercises,
    }
    context={**context1,**context2}
    return render(request, 'workout.html', context)

def profile(request):
    # Get user ID from session
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login_view')  # Redirect to login if user_id is not in session

    try:
        user = Person.objects.get(id=user_id)
    except Person.DoesNotExist:
        user = None

    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_view')

    try:
        user = Person.objects.get(id=user_id)
    except Person.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'User not found'})

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.height = request.POST.get('height', None)
        user.weight = request.POST.get('weight', None)
        user.age = request.POST.get('age', None)
        
        # Handle profile photo upload
        profile_photo = request.FILES.get('profile_photo')
        if profile_photo:
            user.profile_photo.delete()  # Delete old photo if exists
            user.profile_photo = profile_photo

        user.save()
        return redirect('profile')

    context = {
        'user': user
    }
    return render(request, 'edit_profile.html', context)

def logout_view(request):
    # Clear the session data
    request.session.flush()
    # Redirect to the login page or home page after logout
    return redirect('index')

def workout_detail_view(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id)
    except Workout.DoesNotExist:
        return render(request, 'workout_not_found.html')
    
    context = {
        'workout': workout,
    }
    return render(request, 'workout_detail.html', context)

def diet_plan_view(request):
    result = None
    meal_plan = {}

    user_id = request.session.get('user_id')
    user = Person.objects.get(id=user_id)

    if request.method == 'POST':
        age = int(request.POST.get('age'))
        weight = int(request.POST.get('weight'))
        height = int(request.POST.get('height'))
        gender = request.POST.get('gender')
        activity_level = request.POST.get('activity_level')

        # Calculate BMR using Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Calculate TDEE based on activity level
        if activity_level == 'sedentary':
            tdee = bmr * 1.2
        elif activity_level == 'light':
            tdee = bmr * 1.375
        elif activity_level == 'moderate':
            tdee = bmr * 1.55
        elif activity_level == 'active':
            tdee = bmr * 1.725
        elif activity_level == 'very_active':
            tdee = bmr * 1.9
        else:
            tdee = bmr

        # Macronutrient needs
        protein_per_kg = 1.8  # grams of protein per kg of body weight
        total_protein = protein_per_kg * weight  # in grams
        calories_from_protein = total_protein * 4  # 1 gram of protein = 4 kcal

        fat_percentage = 0.30  # 30% of total calories from fat
        calories_from_fat = tdee * fat_percentage
        total_fat = calories_from_fat / 9  # 1 gram of fat = 9 kcal

        calories_from_carbs = tdee - (calories_from_protein + calories_from_fat)
        total_carbs = calories_from_carbs / 4  # 1 gram of carbs = 4 kcal

        # Meal distribution (assuming 4 meals: breakfast, lunch, snack, dinner)
        meal_distribution = {
            'breakfast': 0.25,
            'lunch': 0.30,
            'snack': 0.15,
            'dinner': 0.30
        }

        for meal, fraction in meal_distribution.items():
            meal_calories = tdee * fraction
            meal_protein = total_protein * fraction
            meal_fat = total_fat * fraction
            meal_carbs = total_carbs * fraction

            meal_plan[meal] = {
                'calories': round(meal_calories, 2),
                'protein': round(meal_protein, 2),
                'carbs': round(meal_carbs, 2),
                'fat': round(meal_fat, 2)
            }

        result = f"Your BMR is {bmr:.2f} calories/day.\nYour TDEE based on your activity level is {tdee:.2f} calories/day."

        context1 = {
            'user': user,
            'result': result,
            'meal_plan': meal_plan
        }

        context2={'user':user}
        context={**context1,**context2}

        return render(request, 'diet_plan.html', context)
    
    context={'user':user}

    return render(request, 'diet_plan.html', context)



def calculate_calories(request):

    user_id = request.session.get('user_id')
    user = Person.objects.get(id=user_id)

    if request.method == 'POST':
        age = int(request.POST['age'])
        weight = float(request.POST['weight'])
        height = float(request.POST['height'])
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']

        # Calculate BMR based on gender
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        # Calculate TDEE based on activity level
        activity_levels = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        activity_multiplier = activity_levels.get(activity_level, 1.2)
        daily_calories = bmr * activity_multiplier

        # Render the result in the template
        context1={'result': f'Your estimated daily caloric needs are {daily_calories:.2f} calories to maintain your current weight.'}
        context2={'user':user}
        context={**context1,**context2}
        return render(request, 'calorie_calculate.html', context)
    
    context={'user':user}

    # Render the initial form if GET request
    return render(request, 'calorie_calculate.html',context)

def calculate_bodyfat(request):

    user_id = request.session.get('user_id')
    user = Person.objects.get(id=user_id)
    
    if request.method == 'POST':
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height')) / 100  # Convert height to meters
        age = int(request.POST.get('age', 0))
        gender = request.POST.get('gender')

        # Calculate BMI
        bmi = weight / (height ** 2)

        # Calculate body fat percentage based on BMI and gender
        if gender == 'male':
            body_fat_percentage = 1.20 * bmi + 0.23 * age - 16.2
        else:
            body_fat_percentage = 1.20 * bmi + 0.23 * age - 5.4
        
        context1={'result':round(body_fat_percentage,2)}
        context2={'user':user}
        context={**context1,**context2}

        return render(request,'bodyfat.html',context)
    
    context={'user':user}

    return render(request, 'bodyfat.html',context)


