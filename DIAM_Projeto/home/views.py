from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q

from .models import Post, Comment, Like, Group



# Create your views here.
def index(request):
    latest_post_list = Post.objects.order_by('-post_time')[:5]
    context = {'latest_post_list': latest_post_list, }
    return render(request, 'home/index.html', context)


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


@login_required
def new_post(request):
    context = {'request': request}
    if request.method == 'POST':
        post_title = request.POST['post_title']
        post_content = request.POST['new_post']
        post_time = timezone.now()
        post_new = Post(post_content=post_content, post_time=post_time, author=request.user, post_title=post_title)
        post_new.save()
        return HttpResponseRedirect(reverse('home:index'))
    else:
        return render(request, 'home/new_post.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('home:index')


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    return render(request, 'home/profile.html', {'user': user, 'posts': posts})


def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    liked_post = Like.objects.filter(post=post, user=user).first()
    if not liked_post:
        like_post = Like(post=post, user=user)
        like_post.save()
        post.likes_count += 1
        post.save()
    return redirect('home:index')


@login_required
def write_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        comment_text = request.POST['comment_text']
        user = request.user  # Retrieve the authenticated user

        # Create a new comment instance
        post_time = timezone.now()
        comment = Comment(post=post, user=user, comment_text=comment_text, post_time=post_time)
        comment.save()

        # Redirect to the post details page or any other desired page
        return redirect('home:index')

    return render(request, 'home/write_comment.html', {'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:  # Check if the post belongs to the logged-in user
        post.delete()
    return redirect('home:profile')


@login_required
def create_group(request):
    if request.method == 'POST':
        new_group_name = request.POST.get('group_name')
        if Group.objects.filter(group_name=new_group_name).exists():
            messages.error(request,"A group with that name already exists")
            return render(request, 'home/create_group.html')
        new_admin = request.user
        group_new = Group(admin=new_admin, group_name=new_group_name)
        group_new.save()
        messages.success(request,'Group created successfully!')
        return render(request,'home/group_detail.html',{'group': group_new})
    return render(request,'home/create_group.html')

@login_required
def add_group_member(request, user_username, group_id):
    user = User.objects.get(username=user_username)
    group = Group.objects.get(id=group_id)

    if user not in group.members.all():
        group.members.add(user)
        group.save()

    return redirect('group_detail',group_id=group_id)


def group_detail(request, group_id):
    group = get_object_or_404(Group,id=group_id)
    return render(request,'home/group_detail.html', {'group':group})

def my_groups(request):
    user = request.user
    groups = Group.objects.filter(Q(admin=user) | Q(members=user))
    print(groups)
    return render(request,'home/my_groups.html',{'groups':groups})


