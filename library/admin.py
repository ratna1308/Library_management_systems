from django.contrib import admin
from .models import NormalUser, LibrarianUser, Book, BookRequest


@admin.register(NormalUser)
class NormalUserAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("user",)


@admin.register(LibrarianUser)
class LibrarianUserAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("user",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "stock", "is_available")
    list_filter = ("is_available",)
    search_fields = ("title", "author")


@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "request_date", "renewal_date")
    list_filter = ("request_date", "renewal_date")
    search_fields = ("user__user__username", "book__title")
