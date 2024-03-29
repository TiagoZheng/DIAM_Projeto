from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q

from .models import Post, Comment, Like, Group, GroupPost


# Create your views here.
from django.db.models import Count


def index(request):
    order_by = request.GET.get('order_by', 'time')  # Get the 'order_by' query parameter from the request

    if order_by == 'likes':
        latest_post_list = Post.objects.order_by('-likes_count', '-post_time')[:5]
    else:
        latest_post_list = Post.objects.order_by('-post_time')[:5]

    context = {
        'latest_post_list': latest_post_list,
        'order_by': order_by,
    }
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
        topic = request.POST['topic']
        post_new = Post(post_content=post_content, post_time=post_time, author=request.user,
                        post_title=post_title, topic=topic)
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
    favorite_posts = user.favorite_posts.all()  # Fetch the user's favorite posts
    return render(request, 'home/profile.html', {'user': user, 'posts': posts, 'favorite_posts': favorite_posts})


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
def save_favorite(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user.favorite_posts.filter(pk=post_id).exists():
        # Post is already a favorite, remove it from favorites
        user.favorite_posts.remove(post)
    else:
        # Post is not a favorite, add it to favorites
        user.favorite_posts.add(post)

    return redirect('home:index')



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
def add_group_member(request, group_id):
    context = {'request': request}
    if request.method == 'POST':
        group_member = request.POST['new_group_member']
        try:
            user = get_object_or_404(User, username=group_member)
        except Http404:
            error_msg = f"No user with username '{group_member}' was found."
            context['error'] = error_msg
            return redirect('home:group_detail', group_id=group_id)
        group = Group.objects.get(id=group_id)
        if user not in group.members.all():
            group.members.add(user)
            group.save()
            return redirect('home:my_groups')
        else:
            return render(request, 'home/add_group_member.html', {'group_id': group_id})
    else:
        return render(request, 'home/add_group_member.html', {'group_id': group_id})

@login_required
def group_detail(request, group_id):
    latest_post_list = GroupPost.objects.filter(group_id=group_id)
    group = get_object_or_404(Group,id=group_id)
    return render(request,'home/group_detail.html', {'group':group,'latest_post_list': latest_post_list})

@login_required
def my_groups(request):
    user = request.user
    groups = Group.objects.filter(Q(admin=user) | Q(members=user))
    print(groups)
    return render(request, 'home/my_groups.html', {'groups':groups})

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if group.admin == request.user:  # Check if the group belongs to the logged-in user
        group.delete()
    return redirect('home:my_groups')

@login_required
def delete_member(request, group_id):
    group = get_object_or_404(Group,pk=group_id)
    if request.method=='POST':
        member_username = request.POST['group_member']
        user = get_object_or_404(User,username=member_username)
        group.members.remove(user.id)
        return redirect('home:group_detail',group_id=group_id)
    return render(request,'home/delete_member.html', {'group_id': group_id})

@login_required
def new_group_post(request, group_id):
    if request.method == 'POST':
        post_title = request.POST['post_title']
        post_content = request.POST['post_content']
        topic = request.POST['topic']
        group = Group.objects.get(id=group_id)

        # Check if the user is a member of the group
        if request.user not in group.members.all() and request.user != group.admin:
            return HttpResponseForbidden("You are not a member of this group.")

        # Create a new Post instance
        post = Post.objects.create(
            author=request.user,
            post_title=post_title,
            post_content=post_content,
            post_time=timezone.now(),
            topic=topic
        )

        # Create a new GroupPost instance and associate it with the group and post
        group_post = GroupPost.objects.create(
            group=group,
            post=post
        )

        return redirect('home:group_detail', group_id=group_id)
    else:
        # Handle GET request for displaying the form
        return render(request, 'home/new_group_post.html', {'group_id': group_id})
