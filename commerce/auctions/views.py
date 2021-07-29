from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,bids,auction_listings,comments,watch_list



@login_required(login_url='/login')
def watchlist(request):    
    watch=watch_list.objects.filter(people=request.user)
    return render(request, "auctions/watchlist.html",{"watch":watch})
    
@login_required(login_url='/login')
def mylist(request):    
    item=auction_listings.objects.filter(people=request.user).order_by('-created_at')
    return render(request, "auctions/mylist.html",{"items":item})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required(login_url='/login')
def create(request):
    types= auction_listings.objects.order_by('category').values_list('category', flat=True).distinct()
    if request.method == "POST":
        price=request.POST["price"]
        description = request.POST["comment"]
        url=request.POST["url"]
        title=request.POST["title"]
        if request.POST["add_type"] !="":
            category=request.POST["add_type"]
        else:
            category=request.POST["category"]
            
        auction=auction_listings.objects.create(people=request.user,title=title,image=url,description=description,category=category)
        bids.objects.create(item=auction,price=float(price),people=request.user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html",{"category":types})
        

def show(request):
    types = auction_listings.objects.order_by('category').values_list('category', flat=True).distinct()
    if request.method == "POST":
        category=request.POST["category"]
        if category=="All Category":
            item=auction_listings.objects.all().order_by('-created_at')
            return render(request, "auctions/show.html",{"items":item ,"category":types})
        else:
            item=auction_listings.objects.filter(category=category).order_by('-created_at')
            return render(request, "auctions/show.html",{"items":item ,"category":types})
       
    else :
        
        item=auction_listings.objects.all().order_by('-created_at')
        return render(request, "auctions/show.html",{"items":item,"category":types})
def index(request):
    
    # This list contains a Blog object.
    #>>> Blog.objects.filter(name__startswith='Beatles')
    #<QuerySet [<Blog: Beatles Blog>]>

    # This list contains a dictionary.
    #>>> Blog.objects.filter(name__startswith='Beatles').values()
    #<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
    
    ###選擇目前還有在拍賣的商品
    item = bids.objects.filter(is_closed=False).values('item')
    item_active= auction_listings.objects.filter(id__in = item)
    types = item_active.order_by('category').values_list('category', flat=True).distinct()
    if request.method == "POST":
        category=request.POST["category"]
        if category=="All Category":
            return render(request, "auctions/index.html",{"items":item_active,"category":types})
        else:
            item_active= item_active.filter(category=category)
            return render(request, "auctions/index.html",{"items":item_active,"category":types})
    else:
        return render(request, "auctions/index.html",{"items":item_active,"category":types})
  
@login_required(login_url='/login')
def items(request,title):
    #get() when you want to get a single unique object.
    #filter() when you want to get all objects that match your lookup parameters.
    #get() raises a DoesNotExist exception if an object wasn't found for the given parameters.
    item=auction_listings.objects.get(title=title)
    watch = watch_list.objects.filter(people=request.user,item=item).first()
    cur_price =  bids.objects.filter(item=item).order_by('-created_at').first()
    people_name =bids.objects.filter(item=item).order_by('-created_at').first().people.username
    message=False
    if "add_comment" in request.POST: 
        contents=request.POST["add_comment"]
        comments.objects.create(comment=contents,item=item)
    comment=comments.objects.filter(item=item)
    if "like" in request.POST: 
        
        if request.POST["like"]=="Add To Like":
            watch_list.objects.create(people=request.user,item=item)
        else:
            data = watch_list.objects.get(people=request.user,item=item)
            data.delete()
        return  HttpResponseRedirect(reverse("watchlist"))
    if "price" in request.POST:
        price=request.POST["price"]
        old_price=float(cur_price.price)
        if float(price)>float(old_price):
            bids.objects.create(price=float(price),item=item,people=request.user)
            return  HttpResponseRedirect(reverse("items", args=(title,)))
        else:
            message="Please provide valid input!"
    if "close" in request.POST:
        people_name =bids.objects.filter(item=item).order_by('-created_at').first().people.username
        bids.objects.filter(item=item).update(is_closed=True)

    if bids.objects.filter(item=item).order_by('-created_at').first().is_closed==True:
        final=True
    else:
        final=False
    
    if item.people==request.user:
        add_close=True
        add_bid=False
    else:
        add_close=False
        add_bid=True
    
    if watch==None:
        can_like=True
    else:
        can_like=False
    
    return render(request, "auctions/items.html",{"items":item,"comment":comment,"watch":can_like,"check1":add_close,"check2":add_bid,
                                                     "price":cur_price,"check3":final,"message1":people_name,"message":message})
    
    
