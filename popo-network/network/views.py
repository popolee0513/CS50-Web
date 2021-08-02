from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User,Post
#import requests
#from django.core.mail import send_mail
#from django.core.mail import EmailMultiAlternatives
#from django.template.loader import get_template
from django.conf import settings
from django.db.models import Count, F, Value
import json
from django.db.models import Count
from django.core.paginator import Paginator
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
import re

def password_check(p):
    x = True
    while x:  
        if (len(p)<6 or len(p)>12):
            break
        elif not re.search("[a-z]",p):
            break
        elif not re.search("[0-9]",p):
            break
        elif not re.search("[A-Z]",p):
            break
        elif not re.search("[$#@]",p):
            break
        elif re.search("\s",p):
            break
        else:
            x=False
    return x
    
    

@login_required(login_url='/login')
def follow_control(request):
    if request.method == "POST":
        data = json.loads(request.body)
        state= data["state"]
        people=data["people"]
        cur_user = User.objects.get(username=request.user.username)
        target_user=User.objects.get(id=people)
        
        if state == "follow":
            cur_user.user_following.add(target_user)
            target_user.user_followers.add(cur_user)
            
        else:
            cur_user.user_following.remove(target_user)
            target_user.user_followers.remove(cur_user)
    return JsonResponse({"message": "update follow successfully."}, status=201)
@login_required(login_url='/login')
def create(request):
    # Composing a new email must be via POST
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get("body", "")
        Post.objects.create(author=request.user,content=body)
        return HttpResponseRedirect('/')
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
@login_required(login_url='/login')
def edit(request, article_id):
    if request.method=="PUT":
        data = json.loads(request.body)["content"]
        Post.objects.filter(id=article_id).update(content=data)
        return JsonResponse({"message": "edit successfully."}, status=201)
    elif request.method=="GET":
        data=Post.objects.get(id=article_id).content
        return JsonResponse({"conetnt": data}, status=201)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    
@login_required(login_url='/login')
def following(request):
    cur_user = User.objects.get(username=request.user.username)
    article= Post.objects.filter(author__in=cur_user.user_following.all()).order_by('-created')
    
    paginator = Paginator(article, 10) 
    page_number = request.GET.get('page')
    #Paginator.num_pages：頁面總數。
   
    try:
        article = paginator.page(page_number)
    except PageNotAnInteger:
        article = paginator.page(1)
    except (EmptyPage, InvalidPage):
        article = paginator.page(paginator.num_pages)
    
    return render(request, "network/index.html",{"articles":article,"show_add_post":False,"profile":False})
def index(request):
    article= Post.objects.all().order_by('-created')
    
    paginator = Paginator(article, 10) 
    page_number = request.GET.get('page')
    try:
        article = paginator.page(page_number)
    except PageNotAnInteger:
        article = paginator.page(1)
    except (EmptyPage, InvalidPage):
        article = paginator.page(paginator.num_pages)
    return render(request, "network/index.html",{"articles":article,"show_add_post":True,"profile":False})
@login_required(login_url='/login')
def home(request,user_name):
    if user_name==request.user.username:
        show_add_post=True
    else:
        show_add_post=False
    user=User.objects.get(username=user_name)
    article= Post.objects.filter(author=user).order_by('-created')
    article_count = Post.objects.filter(author=user).count()
    
    paginator = Paginator(article, 10) 
    page_number = request.GET.get('page')
    try:
        article = paginator.page(page_number)
    except PageNotAnInteger:
        article = paginator.page(1)
    except (EmptyPage, InvalidPage):
        article = paginator.page(paginator.num_pages)
    
    follower_count = len(user.user_followers.all())
    followeing_count = len(user.user_following.all())
    follower = list(User.objects.get(username=user_name).user_followers.all().values_list('username', flat=True))
    following= list(User.objects.get(username=user_name).user_following.all().values_list('username', flat=True))
    if request.user not in user.user_followers.all():
        
        check_follow ="follow"
    else:
        check_follow="unfollow"
    
    return render(request, "network/index.html",{"articles":article,"show_add_post":show_add_post,"profile":True,"User":user_name,
    "uid":user.id,"article_count":article_count,"follower_count":follower_count,"followeing_count":followeing_count,"check_follow":check_follow,"follower":follower,"following":following})


def check(request,uid):
     if request.method == "GET":
        
        status=request.GET.get("status")  
        if status=="follower":
            data=list(User.objects.get(id=uid).user_followers.all().values_list('username', flat=True))
            return JsonResponse({"content": data}, status=201)
        else:
     
            data=list(User.objects.get(id=uid).user_following.all().values_list('username', flat=True))
            return JsonResponse({"content": data}, status=201)

def article(request, article_id):
    #data = Post.objects.get(pk=article_id)
    #data.users_like.add(request.user)
    #data = Post.objects.get(pk=article_id).users_like.all()
    #print(data)
    #data = Post.objects.get(pk=article_id)
    #data.users_like.remove(request.user)
    #data = Post.objects.get(pk=article_id).users_like.all()
    #print(len(data))
    if request.method == "PUT":
        if request.user not in Post.objects.get(pk=article_id).users_like.all():
            data=Post.objects.get(pk=article_id)
            data.users_like.add(request.user)
            count=len(Post.objects.get(pk=article_id).users_like.all())
        else:
            data=Post.objects.get(pk=article_id)
            data.users_like.remove(request.user)
            count=len(Post.objects.get(pk=article_id).users_like.all())
        return JsonResponse({"count":count}, status=201)
    elif request.method == "GET":
         count=len(Post.objects.get(pk=article_id).users_like.all())
        
         return JsonResponse({"count":count}, status=201)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    
    
  
    
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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
        
        if email in User.objects.values_list('email', flat=True).distinct():
            return render(request, "network/register.html", {
                "message": "Email already taken."
            })
        """
        response = requests.get(
    "https://isitarealemail.com/api/email/validate",
    params = {'email': email})
        status = response.json()['status']
        if status!="valid":
            return render(request, "network/register.html", {
                "message": "Email is not valid."
            })
       """
        if password_check(password):
            return render(request, "network/register.html", {
                "message": "The password fails to meet the requirements."
            })
        
        # Attempt to create new user
        """
        
            htmly = get_template('network/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome to join us', 'B11000249@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")

            ##################################################################

            try:
                msg.send()
            except:
                print("error in sending mail")
            
        """
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
