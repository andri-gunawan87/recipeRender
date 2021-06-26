from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

from .models import Post, Follow, Profile, Sns_comments
from .forms import UserForm, ProfileForm, PostForm
User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        profile_data = Profile.objects.filter(user = request.user).first()
        friend_request = Follow.objects.filter(following = request.user, friend_request = False)[0:3]
        pending_request = Follow.objects.filter(user = request.user, friend_request = False)[0:3]
        allpost = Post.objects.filter(user=request.user).order_by("-date")
        paginator = Paginator(allpost, 10)
        page = request.GET.get('page', 1)
        user = paginator.page(page)
        if request.method == "GET":
            return render(request, "network/index.html", {
                "form": PostForm,
                "allpost": user,
                "profile_data": profile_data,
                "friend_request": friend_request,
                "pending_request": pending_request,
                })
        else:
            f = Post(user=request.user)
            post_form = PostForm(request.POST, request.FILES, instance=f)
            if post_form.is_valid():
                post_form.save()
                return HttpResponseRedirect(reverse("sns_index"))
            else:
                return render(request, "network/index.html", {
                "form": post_form()
                })
    else:
        allpost = Post.objects.all()
        paginator = Paginator(allpost, 10)
        page = request.GET.get('page', 1)
        user = paginator.page(page)
        return render(request, "network/allpost.html", {
            "allpost": user
            })
            
def all_posts(request):
    profile_data = Profile.objects.filter(user = request.user).first()
    allpost = Post.objects.all()
    paginator = Paginator(allpost, 10)
    page = request.GET.get('page', 1)
    user = paginator.page(page)
    return render(request, "network/allpost.html", {
        "allpost": user,
        "profile_data": profile_data
        })
        
def friends(request, user_id):
    profile_data = Profile.objects.filter(user = request.user).first()
    if request.method == "POST":
        body = request.POST["request"]
        if body == "Confirm":
            a = Follow.objects.get(user=user_id, following=request.user)
            a.friend_request = True
            a.save()
            return render(request, "network/friends.html", {
                "profile_data": profile_data
                })
        elif body == "Delete":
            a = Follow.objects.get(user=user_id, following=request.user)
            a.delete()
            return render(request, "network/friends.html", {
                "profile_data": profile_data
                })            
    else:
        friend_list = Follow.objects.filter(Q(user=user_id) | Q(following=user_id), friend_request=True)
        return render(request, "network/friends.html", {
            "profile_data": profile_data,
            "friend_list": friend_list
            })

def profil(request, user_id):
    user_id = User.objects.get(id=user_id)
    following = Follow.objects.filter(Q(user=user_id) | Q(following=user_id), friend_request=True).values_list("following", flat=True)
    follower = Follow.objects.filter(following=user_id, friend_request=True).values_list("user", flat=True)
    allpost = Post.objects.filter(user=user_id).order_by("-date")
    paginator = Paginator(allpost, 10)
    page = request.GET.get('page', 1)
    user = paginator.page(page)
    if request.user.is_authenticated:
        profile_data = Profile.objects.filter(user = request.user).first()
        friend_request = Follow.objects.filter(user=request.user, following=user_id).first()
        follow = Follow.objects.filter(user=request.user).values_list("following", flat=True)
        return render(request, "network/profile.html", {
            "allpost": user,
            "user_detail": user_id,
            "follow": follow,
            "following": following,
            "follower": follower,
            "friend_request": friend_request,
            "profile_data": profile_data
            })
    else:
        profile_data = Profile.objects.filter(user = user_id).first()
        return render(request, "network/profile.html", {
            "allpost": user,
            "user_detail": user_id,
            "following": following,
            "follower": follower,
            "profile_data": profile_data
            })

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "POST":
        body = request.POST["edit"]
        post = Post.objects.get(id=post_id)
        post.body = body
        post.save()
        return HttpResponse(status=204)
        
def like(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "POST":
        body = request.POST["like"]
        if body == "like":
            post.like_count += 1
            post.save()
            return HttpResponse(status=204)
        else:
            post.like_count -= 1
            post.save()
            return HttpResponse(status=204)

def follow(request):
    user = request.user
    following = Follow.objects.filter(user=request.user).values_list("following", flat=True)
    post = Post.objects.filter(user__in=following)
    if request.method == "GET":
        return render(request, "network/following.html", {
        "allpost": post
        })
    else:
        if "follow" in request.POST:        
            user_id = User.objects.get(id=(request.POST["follow"]))
            f = Follow(user=user, following=user_id)
            f.save()
            return render(request, "network/following.html", {
                "allpost": post
                })
        else:
            user_id = User.objects.get(id=(request.POST["unfollow"]))
            f = Follow.objects.get(user=user, following=user_id)
            f.delete()
            return render(request, "network/following.html", {
                "allpost": post
                })
 
def account(request):
    user_data = request.user
    profile_data = Profile.objects.filter(user=request.user).first()
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        try:
            profile_form = ProfileForm(request.POST, request.FILES, instance=(Profile.objects.get(user=request.user)))
        except Profile.DoesNotExist:
            f = Profile(user=request.user)
            profile_form = ProfileForm(request.POST, instance=f)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            profile_updated = Profile.objects.filter(user=request.user).first()
            return render(request, "network/account.html", {
                "user_data": user_data,
                "profile_data": profile_updated
                })
        else:
            return render(request, "network/account.html", {
                "a": "Please correct the error below",
                "user_data": user_data,
                "profile_data": profile_data
                })
    else:        
        return render(request, "network/account.html", {
            "user_data": user_data,
            "profile_data": profile_data,
            "b": ProfileForm
        })
        
def comments(request, item_id):
    post = Post.objects.get(id=item_id)    
    try:
        comments = Sns_comments.objects.filter(post=post).order_by('-date')
    except Sns_comments.DoesNotExist:
        comments = None
    if request.user.is_authenticated:
        profile_data = Profile.objects.filter(user=request.user).first()
        if request.method == "POST":
            body = request.POST["comments"]
            a = Sns_comments(user=request.user, post=post, body=body)
            a.save()
            return render(request, "network/comments.html", {
                "profile_data": profile_data,
                "comments": comments,
                "post": post,
            })
        else:
            return render(request, "network/comments.html", {
                    "profile_data": profile_data,
                    "comments": comments,
                    "post": post
                })
    else:
        a = post.user.id
        profile_data = Profile.objects.filter(user=a).first()
        return render(request, "network/comments.html", {
                        "profile_data": profile_data,
                        "comments": comments,
                        "post": post
                    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("sns_index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("sns_index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        elif User.objects.filter(email=email).exists():
            return render(request, "network/register.html", {
                "message": "Email address already taken."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("sns_index"))
    else:
        return render(request, "network/register.html")
