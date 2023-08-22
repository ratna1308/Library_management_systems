from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, BookRequest, NormalUser
from .forms import BookRequestForm, BookForm
from django.contrib.auth import logout
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def home(request):
    books = Book.objects.all()
    user_requests = BookRequest.objects.filter(user__user=request.user)
    return render(
        request, "library/home.html", {"books": books, "user_requests": user_requests}
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def request_book(request, book_id=None):
    if book_id is not None:
        book = get_object_or_404(Book, pk=book_id)
        if request.method == "POST":
            form = BookRequestForm(request.POST)
            if form.is_valid():
                normal_user = NormalUser.objects.get(user=request.user)
                book_request = form.save(commit=False)
                book_request.user = normal_user
                book_request.book = book
                book_request.save()
                messages.success(request, "Book requested successfully.")
                return redirect("home")
        else:
            form = BookRequestForm()
        return render(
            request, "library/request_book.html", {"form": form, "book": book}
        )
    else:
        if request.method == "POST":
            form = BookRequestForm(request.POST)
            if form.is_valid():
                normal_user = NormalUser.objects.get(user=request.user)
                book_request = form.save(commit=False)
                book_request.user = normal_user
                book_request.save()
                messages.success(request, "Book requested successfully.")
                return redirect("home")
        else:
            form = BookRequestForm()
        return render(
            request, "library/request_book.html", {"form": form, "book": None}
        )


@login_required
def request_new_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New book request submitted successfully.")
            return redirect("home")
    else:
        form = BookForm()
    return render(request, "library/request_book.html", {"form": form, "book": None})


@login_required
def librarian_dashboard(request):
    return render(request, "library/librarian_dashboard.html")


@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect("librarian_dashboard")
    else:
        form = BookForm()
    return render(request, "library/add_book.html", {"form": form})


@login_required
def approve_request(request, request_id):
    book_request = get_object_or_404(BookRequest, pk=request_id)
    book_request.renewal_date = None
    book_request.save()
    messages.success(request, "Book request approved.")
    return redirect("librarian_dashboard")


@login_required
def assigned_books(request):
    assigned_books = BookRequest.objects.filter(renewal_date__isnull=False)
    return render(
        request, "library/assigned_books.html", {"assigned_books": assigned_books}
    )


@login_required
def revoke_assignment(request, request_id):
    book_request = get_object_or_404(BookRequest, pk=request_id)
    book_request.renewal_date = None
    book_request.save()
    messages.success(request, "Assignment revoked successfully.")
    return redirect("assigned_books")


@login_required
def view_book_details(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "library/view_book_details.html", {"book": book})


@receiver(post_save, sender=User)
def create_or_update_normal_user(sender, instance, created, **kwargs):
    if created:
        NormalUser.objects.create(user=instance)
    else:
        instance.normaluser.save()
