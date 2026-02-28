from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta

from .models import Book, Author, Category, Borrowing, Review, UserProfile, Contact
from .forms import RegistrationForm, LoginForm, ContactForm, ReviewForm, ProfileEditForm



def home(request):
    latest_books = Book.objects.all()[:6]
    top_rated_books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:3]
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_students = User.objects.filter(is_staff=False).count()

    context = {
        'latest_books': latest_books,
        'top_rated_books': top_rated_books,
        'total_books': total_books,
        'total_authors': total_authors,
        'total_students': total_students,
    }
    return render(request, 'library/home.html', context)


def all_books(request):
    books = Book.objects.all()
    search_query = request.GET.get('q', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | Q(author__name__icontains=search_query)
        )

    category_id = request.GET.get('category', '')
    if category_id:
        books = books.filter(category_id=category_id)

    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        books = books.order_by('created_at')
    elif sort_by == 'highest_rated':
        books = books.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        books = books.order_by('-created_at')

    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    for cat in categories:
        cat.is_selected = (str(cat.id) == category_id)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'sort_by': sort_by,
        'sort_newest': sort_by == 'newest',
        'sort_oldest': sort_by == 'oldest',
        'sort_highest_rated': sort_by == 'highest_rated',
    }
    return render(request, 'library/books.html', context)


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = book.reviews.all()
    user_has_borrowed = False
    user_currently_borrowed = False
    user_has_reviewed = False

    if request.user.is_authenticated:
        user_has_borrowed = Borrowing.objects.filter(user=request.user, book=book).exists()
        user_currently_borrowed = Borrowing.objects.filter(
            user=request.user, book=book, returned=False
        ).exists()
        user_has_reviewed = Review.objects.filter(user=request.user, book=book).exists()

    context = {
        'book': book,
        'reviews': reviews,
        'user_has_borrowed': user_has_borrowed,
        'user_currently_borrowed': user_currently_borrowed,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'library/book_detail.html', context)


def categories_page(request):
    categories = Category.objects.annotate(num_books=Count('books'))
    context = {'categories': categories}
    return render(request, 'library/categories.html', context)


def category_books(request, id):
    category = get_object_or_404(Category, id=id)
    books = Book.objects.filter(category=category)

    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'library/category_books.html', context)


def authors_page(request):
    authors = Author.objects.annotate(num_books=Count('books'))
    context = {'authors': authors}
    return render(request, 'library/authors.html', context)


def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    books = Book.objects.filter(author=author)
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'library/author_detail.html', context)


def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'library/contact.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'library/login.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            
            name_parts = form.cleaned_data['full_name'].split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.save()

            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', '')
            )

            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to the library.')
            return redirect('home')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'library/register.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')



@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {'profile': profile}
    return render(request, 'library/profile.html', context)


@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            name_parts = form.cleaned_data['full_name'].split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.email = form.cleaned_data['email']

            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)

            user.save()

            profile.phone = form.cleaned_data.get('phone', '')
            if form.cleaned_data.get('profile_picture'):
                profile.profile_picture = form.cleaned_data['profile_picture']
            profile.save()

            if new_password:
                login(request, user)

            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileEditForm(initial={
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
            'phone': profile.phone,
        })

    context = {'form': form, 'profile': profile}
    return render(request, 'library/profile_edit.html', context)



@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.is_available:
        messages.error(request, 'Sorry, this book is not available for borrowing.')
        return redirect('book_detail', id=book.id)

    if Borrowing.objects.filter(user=request.user, book=book, returned=False).exists():
        messages.warning(request, 'You have already borrowed this book.')
        return redirect('book_detail', id=book.id)

    current_borrowings = Borrowing.objects.filter(user=request.user, returned=False).count()
    if current_borrowings >= 5:
        messages.error(request, 'You have reached the maximum borrowing limit (5 books).')
        return redirect('book_detail', id=book.id)

    due_date = timezone.now() + timedelta(days=14)
    Borrowing.objects.create(
        user=request.user,
        book=book,
        due_date=due_date,
    )

    book.available_copies -= 1
    book.save()

    messages.success(request, f'You have successfully borrowed "{book.title}". Please return it by {due_date.strftime("%B %d, %Y")}.')
    return redirect('my_books')


@login_required
def my_books(request):
    borrowings = Borrowing.objects.filter(user=request.user, returned=False)
    past_borrowings = Borrowing.objects.filter(user=request.user, returned=True)

    context = {
        'borrowings': borrowings,
        'past_borrowings': past_borrowings,
    }
    return render(request, 'library/my_books.html', context)


@login_required
def return_book(request, borrowing_id):
    """Return a borrowed book."""
    borrowing = get_object_or_404(Borrowing, id=borrowing_id, user=request.user)

    if borrowing.returned:
        messages.warning(request, 'This book has already been returned.')
        return redirect('my_books')

    borrowing.returned = True
    borrowing.return_date = timezone.now()
    borrowing.save()

    book = borrowing.book
    book.available_copies += 1
    book.save()

    messages.success(request, f'You have successfully returned "{book.title}".')
    return redirect('my_books')



@login_required
def add_review(request, id):
    book = get_object_or_404(Book, id=id)

    if not Borrowing.objects.filter(user=request.user, book=book).exists():
        messages.error(request, 'You can only review books you have borrowed.')
        return redirect('book_detail', id=book.id)

    if Review.objects.filter(user=request.user, book=book).exists():
        messages.warning(request, 'You have already reviewed this book.')
        return redirect('book_detail', id=book.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('book_detail', id=book.id)
    else:
        form = ReviewForm()

    context = {'form': form, 'book': book}
    return render(request, 'library/add_review.html', context)
