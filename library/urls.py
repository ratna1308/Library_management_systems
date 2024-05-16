from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path('login/', views.user_login, name='login'),
    path("request_book/", views.request_book, name="request_book"),
    path('request_book/<int:book_id>/', views.request_book, name='request_book'),
    path("librarian_dashboard/", views.librarian_dashboard, name="librarian_dashboard"),
    path("add_book/", views.add_book, name="add_book"),
    path('approve_request/', views.approve_request, name='approve_request'),
    path("assigned_books/", views.assigned_books, name="assigned_books"),
    path("view_book_details/<int:book_id>/",views.view_book_details,name="view_book_details",),
    path("logout/", views.logout_view, name="logout"),
]
