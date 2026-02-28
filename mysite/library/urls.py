from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.all_books, name='all_books'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('categories/', views.categories_page, name='categories'),
    path('category/<int:id>/', views.category_books, name='category_books'),
    path('authors/', views.authors_page, name='authors'),
    path('author/<int:id>/', views.author_detail, name='author_detail'),
    path('contact/', views.contact_page, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('my-books/', views.my_books, name='my_books'),
    path('return/<int:borrowing_id>/', views.return_book, name='return_book'),
    path('book/<int:id>/review/', views.add_review, name='add_review'),
]
