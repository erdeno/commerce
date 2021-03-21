from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuctionListView.as_view(), name="index"),
    path("item/<int:pk>", views.AuctionDetailView.as_view(), name="item"),
    path("category/<int:category_id>", views.category_detail, name="category_detail"),
    path("create", views.create, name="create"),
    path("create_category", views.create_category, name="create_category"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("make_bid/<int:item_id>", views.make_bid, name="make_bid"),
    path(
        "add_to_watchlist/<int:item_id>",
        views.add_to_watchlist,
        name="add_to_watchlist",
    ),
    path(
        "remove_from_watchlist/<int:item_id>",
        views.remove_from_watchlist,
        name="remove_from_watchlist",
    ),
    path("make_comment/<int:item_id>", views.make_comment, name="make_comment"),
    path("close_auction/<int:item_id>", views.close_auction, name="close_auction"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
