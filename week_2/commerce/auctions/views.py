from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Bid, Listing, Comment


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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


def create(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        image = request.POST['image']
        category = request.POST['category']
        current_bid = request.POST['bid']
        user = request.user

        category_type = Category.objects.get(type=category)

        bid = Bid(
            bidder=user,
            bid=float(current_bid)
        )
        bid.save()

        listing = Listing(
            title=title,
            description=description,
            owner=user,
            actual_bid=bid,
            image=image,
            category=category_type
        )
        listing.save()
        return HttpResponseRedirect(reverse(index))


def listing(request, id):
    listing = Listing.objects.get(pk=id)
    listing_in_watchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.all()
    return render(request, "auctions/listing.html", {
        'listing': listing,
        "watchlist": listing_in_watchlist,
        "comments": comments
    })


def addWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def removeWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlist(request):
    user = request.user
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def addComment(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    message = request.POST['comment']

    comment = Comment(
        author=user,
        item=listing,
        message=message
    )
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))
