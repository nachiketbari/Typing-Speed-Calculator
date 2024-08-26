
from django.shortcuts import render, HttpResponse, redirect,  get_object_or_404
from typingtest import views
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import time
from django.contrib import messages
# from .models import 
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            u = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
            u.set_password(password)
            u.save()
            return redirect('/')
        else:
            context = {}
            context['error'] = "Password and Confirm Password do not match"
            return render(request, 'register.html', context)

def user_login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context = {}
            context['error'] = "Username and Password is incorrect"
            return render(request, 'login.html', context)
@login_required
def user_logout(request):
    logout(request)
    return redirect("/")


# def typing_test_view(request):
#     if request.method == 'POST':
#         # Get the start time from the form and handle any potential issues
#         try:
#             start_time = float(request.POST.get('start_time', '0'))
#         except ValueError:
#             start_time = 0
        
#         typed_text = request.POST.get('typed_text', '')
        
#         # Predefined test text
#         test_text = "The quick brown fox jumps over the lazy dog."
        
#         # Calculate end time and duration
#         end_time = time.time()
#         time_taken = end_time - start_time
        
#         # Calculate Words Per Minute (WPM)
#         words = len(typed_text.split())
#         wpm = (words / time_taken) * 60 if time_taken > 0 else 0
        
#         # Accuracy calculation
#         correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(test_text) and c == test_text[i])
#         accuracy = (correct_chars / len(test_text)) * 100 if len(test_text) > 0 else 0
        
#         context = {
#             'wpm': round(wpm, 2),
#             'accuracy': round(accuracy, 2),
#             'time_taken': round(time_taken, 2),
#             'test_text': test_text,
#             'typed_text': typed_text,
#         }
        
#         return render(request, 'typing_test_result.html', context)


@login_required(login_url='/login')  # Redirects to login page if the user is not logged in
def typing_test_view(request):
    if request.method == 'POST':
        start_time = float(request.POST.get('start_time', 0))
        typed_text = request.POST.get('typed_text', '')

        # Predefined test text
        test_text = "The quick brown fox jumps over the lazy dog."

        # Calculate end time and duration
        end_time = time.time()
        time_taken = end_time - start_time

        # Calculate words per minute (WPM)
        words = len(test_text.split())
        wpm = (words / time_taken) * 60

        # Accuracy calculation
        correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(test_text) and c == test_text[i])
        accuracy = (correct_chars / len(test_text)) * 100

        context = {
            'wpm': wpm,
            'accuracy': accuracy,
            'time_taken': time_taken,
            'test_text': test_text,
            'typed_text': typed_text,
        }

        return render(request, 'typing_test_result.html', context)

    # Render initial form
    test_text = "The quick brown fox jumps over the lazy dog."
    context = {'test_text': test_text}
    return render(request, 'typing_test.html', context)
    
    # Render the initial typing test form
    test_text = "The quick brown fox jumps over the lazy dog."
    context = {'test_text': test_text}
    return render(request, 'typing_test.html', context)

def typing_test_result_view(request):
    if request.method == 'POST':
        # Get the start time, end time, and user input from the POST data
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        typed_text = request.POST.get('typed_text')
        original_text = request.POST.get('original_text')
        
        # Convert time from string to float
        start_time = float(start_time)
        end_time = float(end_time)
        
        # Calculate the time taken in seconds
        time_taken = end_time - start_time
        
        # Calculate words per minute (WPM)
        words_count = len(typed_text.split())
        minutes = time_taken / 60
        wpm = words_count / minutes
        
        # Calculate accuracy
        correct_chars = 0
        for i in range(min(len(typed_text), len(original_text))):
            if typed_text[i] == original_text[i]:
                correct_chars += 1
        
        accuracy = (correct_chars / len(original_text)) * 100 if len(original_text) > 0 else 0
        
        # Prepare the context for rendering the result page
        context = {
            'wpm': round(wpm, 2),
            'accuracy': round(accuracy, 2),
            'time_taken': round(time_taken, 2),
            'typed_text': typed_text,
            'original_text': original_text,
        }
        
        # Render the result template with the context
        return render(request, 'typing_test_result.html', context)
    else:
        return HttpResponse("Invalid request method")