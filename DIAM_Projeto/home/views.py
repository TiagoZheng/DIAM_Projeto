from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request, 'home/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to success page or some other URL TODO
            return redirect('success')
        else:
            # Return invalid an invalid login message
            return render(request, 'home/login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'home/login.html')


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        # Check if password matches
        if confirm_password != password:
            return render(request, 'home/registration.html', {'error': 'Password does not match.'})

        # Create the user
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except:
            return render(request, 'home/registration.html', {'error': 'Failed to register'})

        # If success
        return redirect('success')

    else:
        return render(request, 'home/registration.html')
