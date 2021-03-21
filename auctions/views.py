from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.core.paginator import Paginator

from django.contrib import messages

from django.contrib.auth.decorators import login_required


from .models import User, Listing, Category, Bid, Comment
from .forms import ListingForm


class AuctionListView(ListView):
    model = Listing
    template_name = "auctions/index.html"
    paginate_by = 3


class AuctionDetailView(DetailView):
    model = Listing
    template_name = "auctions/item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # item = get_object_or_404(Listing, pk=self.kwargs["pk"])
        comments = Comment.objects.filter(comment_item=self.kwargs["pk"]).all()
        context["comments"] = comments
        return context


def categories(request):
    categories = Category.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(categories, 10)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
    return render(request, "auctions/categories.html", {"categories": categories})


def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)
    items_in_category = Listing.objects.filter(category=category_id).all()
    page = request.GET.get("page", 1)
    paginator = Paginator(items_in_category, 9)
    try:
        items_in_category = paginator.page(page)
    except PageNotAnInteger:
        items_in_category = paginator.page(1)
    except EmptyPage:
        items_in_category = paginator.page(paginator.num_pages)
    return render(
        request,
        "auctions/category_detail.html",
        {
            "items_in_category": items_in_category,
            "category": category,
        },
    )


@login_required
def create_category(request):
    new_category = request.POST.get("newCategory")
    c = Category(category_name=new_category, item_count=0)
    c.save()
    return HttpResponseRedirect(reverse("categories"))


@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            starting_price = form.cleaned_data["starting_price"]
            listing = form.save(commit=False)
            listing.current_price = starting_price

            listing.created_by = User.objects.get(pk=request.user.id)
            listing.is_active = True
            listing.save()
            c = Category.objects.get(pk=category.id)
            items = Listing.objects.filter(category=c.id).all()
            c.item_count = items.count()
            c.save()
            messages.success(request, "Listing created successfully.")
            return HttpResponseRedirect(reverse("index"))

    else:
        form = ListingForm()
    return render(request, "auctions/create.html", {"form": form})


@login_required
def watchlist(request):
    items = Listing.objects.filter(watchers=request.user.id)
    page = request.GET.get("page", 1)
    paginator = Paginator(items, 9)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, "auctions/watchlist.html", {"items": items})


@login_required
def add_to_watchlist(request, item_id):
    user = User.objects.get(pk=request.user.id)
    item = Listing.objects.get(pk=item_id)
    item.watchers.add(user)
    item.save()
    items = Listing.objects.filter(watchers=user)
    user.watchlist_item_count = items.count()
    user.save()
    return HttpResponseRedirect(reverse("item", kwargs={"pk": item_id}))


@login_required
def make_bid(request, item_id):
    item = Listing.objects.get(pk=item_id)
    previous_bids = [i.bid_amount for i in Bid.objects.filter(bid_item=item).all()]
    if previous_bids:
        max_previous_bids = max(previous_bids)
    else:
        max_previous_bids = 0
    bidder = User.objects.get(pk=request.user.id)
    new_bid_amount = int(request.POST.get("newBid"))
    if new_bid_amount >= item.starting_price and new_bid_amount > max_previous_bids:
        new_bid = Bid(bidder=bidder, bid_amount=new_bid_amount, bid_item=item)
        new_bid.save()
        item.last_bidder = bidder
        item.current_price += new_bid.bid_amount
        item.save()
    else:
        messages.warning(
            request,
            f"The bid must greater than ${max([item.starting_price, max_previous_bids])}!",
        )

    return HttpResponseRedirect(reverse("item", kwargs={"pk": item_id}))


@login_required
def remove_from_watchlist(request, item_id):
    user = User.objects.get(pk=request.user.id)
    item = Listing.objects.get(pk=item_id)
    item.watchers.remove(user)
    item.save()
    items = Listing.objects.filter(watchers=user)
    user.watchlist_item_count = len(items)
    user.save()
    return HttpResponseRedirect(reverse("item", kwargs={"pk": item_id}))


@login_required
def make_comment(request, item_id):
    item = Listing.objects.get(pk=item_id)
    title = request.POST.get("title")
    content = request.POST.get("content")
    rate = request.POST.get("rate")
    c = Comment(
        title=title,
        comment_user=request.user,
        comment_item=item,
        content=content,
        rate=rate,
    )
    c.save()
    return HttpResponseRedirect(reverse("item", kwargs={"pk": item_id}))


@login_required
def close_auction(request, item_id):
    item = Listing.objects.get(pk=item_id)
    if request.user.id == item.created_by.id and item.is_active:
        item.is_active = False
        item.save()

    return HttpResponseRedirect(reverse("item", kwargs={"pk": item_id}))


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, watchlist_item_count=0
            )
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
