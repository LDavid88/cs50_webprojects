from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listings, Bids


def index(request):
    listings = Listings.objects.all()
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
        bid = request.POST['bid']
        image = request.POST['image']
        category = Category.objects.get(type=request.POST["category"])
        user = request.user

        listing = Listings(
            title=title,
            description=description,
            image=image,
            price=bid,
            category=category,
            user=user
        )
        listing.save()
        return HttpResponseRedirect(reverse(index))


def listing(request, id):
    listing = Listings.objects.get(pk=id)
    user_watchlist = request.user in listing.watchlist.all()
    starting_bid = listing.price
    bidder = request.user
    if request.method == "POST":
        new_bid = float(request.POST["newBid"])
        if new_bid >= starting_bid:
            bid = Bids(
                bidder=bidder,
                bid=new_bid,
                article=listing
            )
            bid.save()
            add_watchlist(request, id)
            return HttpResponseRedirect(reverse(index))
        else:
            return HttpResponse("Bid should be equal or greater than the starting bid")
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": user_watchlist,
            "bidder": bidder
        })


def add_watchlist(request, id):
    listing = Listings.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def remove_watchlist(request, id):
    listing = Listings.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlist(request):
    user = request.user
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
