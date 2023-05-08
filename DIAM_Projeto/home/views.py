from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone

from .models import Post


# Create your views here.
def index(request):
    latest_post_list = Post.objects.order_by('-post_time')[:5]
    context = {'latest_post_list': latest_post_list, }
    return render(request, 'home/index.html', context)


def details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # return HttpResponse("Esta e a questao %s." % questao_id)
    return render(request, 'home/index', {'post': post})


def results(request, post_id):
    response = "Estes sao os resultados da questao %s."
    return HttpResponse(response % post_id)


def likes(request, post_id):
    return HttpResponse("Votacao na questao %s." % post_id)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to success page or some other URL TODO
            return HttpResponseRedirect(reverse('home:index'))
        else:
            # Return invalid an invalid login message
            return render(request, 'home/login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'home/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        # Check if password matches
        if confirm_password != password:
            return render(request, 'home/register.html', {'error': 'Password does not match.'})

        # Create the user
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
        except:
            return render(request, 'home/register.html', {'error': 'Failed to register'})

        # If success
        return HttpResponseRedirect(reverse('home:index'))

    else:
        return render(request, 'home/register.html')


def new_post(request):
    if request.method == 'POST':
        post_content = request.POST['new_post']
        post_time = timezone.now()
        post_new = Post(post_content=post_content, post_time=post_time)
        post_new.save()
        return HttpResponseRedirect(reverse('home:index'))
    else:
        return render(request, 'home/new_post.html')


def user_logout(request):
    logout(request)
    return redirect('home:index')


@login_required
def profile(request):
    user = request.user
    return render(request, 'home/profile.html', {'user': user})
