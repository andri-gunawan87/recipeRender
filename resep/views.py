from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse
from .models import User, Recipe, Favorite, Comment, Likes
from django.core.paginator import Paginator
import requests
import json
from django.http import JsonResponse
import random
from random import sample

# Create your views here.

def index(request):
    a = Recipe.objects.order_by("-id")[:8]
    b = Recipe.objects.order_by("like_count")[:3]
    c = Comment.objects.order_by("-time")[:3]
    return render(request, "resep/index.html", {
        "data": a,
        "carousel": b,
        "comments": c
    })
        
def new_recipe(request):
    a = Recipe.objects.count()
    b = random.sample(range(1, a), 3)
    c = Recipe.objects.filter(id__in=b)
    if request.method == "POST":
        d = request.POST.getlist("ing")
        e = request.POST.getlist("step")
        f = Recipe(
        user = request.user,
        title = request.POST["rec_name"],
        key = request.POST["rec_name"],
        image = request.POST["rec_img"],
        difficulty = request.POST["rec_dif"],
        times = request.POST["rec_time"],
        desc = request.POST["rec_name"],
        ingredient = d,
        step = e,
        )
        f.save()
        return HttpResponseRedirect(reverse("index"))       
    else:
        return render(request, "resep/new_recipe.html", {
        "data": c
        })
    
def all_recipe(request):
    a = Recipe.objects.all()
    paginator = Paginator(a, 8)
    page = request.GET.get('page', 1)
    user = paginator.page(page)
    b = Comment.objects.order_by("-time")[:3]
    return render(request, "resep/all_recipe.html", {
        "data": user,
        "comments": b
    })
    
def profile(request, user_id):
    a = Recipe.objects.filter(user=user_id)
    paginator = Paginator(a, 8)
    page = request.GET.get('page', 1)
    user = paginator.page(page)
    b = Favorite.objects.filter(user=user_id, fav=True)
    c = Comment.objects.filter(user=user_id)
    return render(request, "resep/profile.html", {
        "data": user,
        "data_all": a,
        "fav": b,
        "comments": c
    })
    
def detail(request, recipe_id):
    a = Recipe.objects.get(id=recipe_id)
    c = Comment.objects.filter(rec=a).order_by("-time")    
    if request.user.is_authenticated:
        b = Favorite.objects.filter(user=request.user, rec=a).first()
        try:
            d = Likes.objects.get(user=request.user, rec=a)
        except: 
            d = None
        return render(request, "resep/detail.html", {
            "data": a,
            "favorite": b,
            "comments": c,
            "likes": d
        })
    else:
        return render(request, "resep/detail.html", {
            "data": a,
            "comments": c
        })
    
def favorite(request):
    user_id = request.user    
    if request.method == "POST":
        fav_data = request.POST["fav"]
        rec = Recipe.objects.get(id=fav_data)
        try:
            favor = Favorite.objects.get(user=user_id, rec=rec)
            if favor.fav == True:
                favor.fav = False
                favor.save()
                return redirect("detail", recipe_id=rec.id)
            elif favor.fav == False:
                favor.fav = True
                favor.save()
                return redirect("detail", recipe_id=rec.id)
        except Favorite.DoesNotExist:
            f = Favorite(user=user_id, rec=rec, fav=True)
            f.save()
            return redirect("detail", recipe_id=rec.id)
    else:
        f = favorite.objects.filter(user=user_id, fav=True)
        return render(request, "resep/favorite.html", {
            "list": f
            })

def addcomment(request):
    user_id = request.user
    list_id = request.POST["data_id"]
    if request.method == "POST":
        comment_data = request.POST["textarea"]        
        f = Recipe.objects.get(id=list_id)
        g = Comment(user=user_id, rec=f, comment=comment_data)
        g.save()
        return HttpResponseRedirect(reverse("detail", args=(list_id,)))
    else:
        return redirect("index")
 
def search(request):
    name = request.GET['q']
    a = Recipe.objects.filter(title__icontains=name)
    paginator = Paginator(a, 5)
    page = request.GET.get('page', 1)
    user = paginator.page(page)
    b = Recipe.objects.count()
    c = random.sample(range(1, b), 3)
    d = Recipe.objects.filter(id__in=c)
    return render(request, "resep/search.html", {
        "data": user,
        "search": name,
        "comments": d
    })

def like(request, post_id):
    a = Recipe.objects.get(id=post_id)
    if request.method == "GET":
        return JsonResponse(a.serialize())
    elif request.method == "POST":
        body = request.POST["like"]
        try:
            b = Likes.objects.get(user=request.user, rec=a)
        except: 
            b = Likes(user=request.user, rec=a)
        if body == "like":
            a.like_count += 1
            a.save()
            b.like = True
            b.dislike = False
            b.save()
            return HttpResponse(status=204)
        else:
            a.like_count -= 1
            a.save()
            b.like = False
            b.dislike = True
            b.save()
            return HttpResponse(status=204)
 
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "resep/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        a = Recipe.objects.count()
        b = random.sample(range(1, a), 3)
        c = Recipe.objects.filter(id__in=b)
        return render(request, "resep/login.html", {
            "data": c
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    a = Recipe.objects.count()
    b = random.sample(range(1, a), 3)
    c = Recipe.objects.filter(id__in=b)
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "resep/register.html", {
                "data": c,
                "message": "Passwords must match."
            })
        elif User.objects.filter(email=email).exists():
            return render(request, "resep/register.html", {
                "data": c,
                "message": "Email address already taken."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "resep/register.html", {
                "data": c,
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "resep/register.html", {
        "data": c
        })
