from django.contrib import admin
from .models import Author, Category, Book, UserProfile, Borrowing, Review, Contact, VisitLog


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count', 'created_at')
    search_fields = ('name', 'bio')
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'book_count', 'created_at')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_year', 'total_copies', 'available_copies', 'average_rating', 'created_at')
    list_filter = ('category', 'author', 'language', 'publication_year')
    search_fields = ('title', 'author__name', 'description')
    list_per_page = 20
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'category', 'description', 'cover_image')
        }),
        ('Details', {
            'fields': ('publication_year', 'pages', 'language')
        }),
        ('Inventory', {
            'fields': ('total_copies', 'available_copies')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'currently_borrowed_count', 'total_borrowed_count', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_per_page = 20


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'return_date', 'returned', 'is_overdue')
    list_filter = ('returned', 'borrow_date')
    search_fields = ('user__username', 'book__title')
    list_per_page = 20


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'book__title', 'comment')
    list_per_page = 20


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    list_per_page = 20


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('path', 'method', 'ip_address', 'user', 'timestamp')
    list_filter = ('method', 'timestamp')
    search_fields = ('path', 'ip_address')
    list_per_page = 50
