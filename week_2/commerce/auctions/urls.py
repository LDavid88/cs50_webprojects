from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("addWatchlist/<str:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<str:id>", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addComment/<str:id>", views.addComment, name="addComment"),
    path("newBid/<str:id>", views.newBid, name="newBid"),
    path("closeAuction/<str:id>", views.closeAuction, name="closeAuction")
]
