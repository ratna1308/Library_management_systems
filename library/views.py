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
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta



@login_required
def home(request):
    books = Book.objects.all()
    user_requests = BookRequest.objects.filter(user__user=request.user)
    return render(
        request, "library/home.html", {"books": books, "user_requests": user_requests}
    )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')  # Default redirect to 'home' if 'next' is not present
            return redirect(next_url)
        else:
            return HttpResponse("Invalid login. Please try again.")
    else:
        return render(request, 'library/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login') 


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


# @login_required
# def request_new_book(request):
#     if request.method == "POST":
#         form = BookForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "New book request submitted successfully.")
#             return redirect("home")
#     else:
#         form = BookForm()
#     return render(request, "library/request_book.html", {"form": form, "book": None})


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
def approve_request(request):
    # Fetch unapproved book requests
    unapproved_requests = BookRequest.objects.filter(renewal_date__isnull=True)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        book_request = get_object_or_404(BookRequest, pk=request_id)
        book_request.renewal_date = timezone.now()  # Setting renewal_date to mark as approved/assigned
        book_request.save()
        messages.success(request, f"Book request for '{book_request.book.title}' approved successfully.")
        return redirect("librarian_dashboard")

    return render(request, "library/approve_request.html", {"requests": unapproved_requests})


@login_required
def assigned_books(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')
        book_request = get_object_or_404(BookRequest, pk=request_id)

        if action == 'renew':
            book_request.renewal_date = timezone.now() + timedelta(days=10)
            book_request.save()
            messages.success(request, f"Renewal for '{book_request.book.title}' has been processed.")

        elif action == 'remove':
            book_request.renewal_date = None
            book_request.book.is_available = True
            book_request.book.save()
            book_request.save()
            messages.success(request, f"'{book_request.book.title}' has been returned to stock.")

        return redirect('assigned_books')

    assigned_books = BookRequest.objects.filter(renewal_date__isnull=False)
    return render(request, "library/assigned_books.html", {"assigned_books": assigned_books})


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
