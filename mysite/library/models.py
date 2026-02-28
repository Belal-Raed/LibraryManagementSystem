from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name="Author Name")
    bio = models.TextField(blank=True, verbose_name="Biography")
    photo = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name="Photo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name

    def book_count(self):
        return self.books.count()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    icon = models.CharField(max_length=50, default='fas fa-book', verbose_name="Icon Class")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def book_count(self):
        return self.books.count()


class Book(models.Model):
    title = models.CharField(max_length=300, verbose_name="Book Title")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', verbose_name="Author")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name="Category")
    description = models.TextField(blank=True, verbose_name="Description")
    cover_image = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name="Cover Image")
    publication_year = models.PositiveIntegerField(default=2024, verbose_name="Publication Year")
    pages = models.PositiveIntegerField(default=0, verbose_name="Number of Pages")
    language = models.CharField(max_length=50, default='English', verbose_name="Language")
    total_copies = models.PositiveIntegerField(default=1, verbose_name="Total Copies")
    available_copies = models.PositiveIntegerField(default=1, verbose_name="Available Copies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.available_copies > 0

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(avg=models.Avg('rating'))['avg'], 1)
        return 0

    @property
    def rating_count(self):
        return self.reviews.count()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Profile Picture")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile: {self.user.username}"

    @property
    def currently_borrowed_count(self):
        return self.user.borrowings.filter(returned=False).count()

    @property
    def total_borrowed_count(self):
        return self.user.borrowings.count()


class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowings', verbose_name="Student")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings', verbose_name="Book")
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name="Borrow Date")
    due_date = models.DateTimeField(verbose_name="Due Date")
    return_date = models.DateTimeField(null=True, blank=True, verbose_name="Return Date")
    returned = models.BooleanField(default=False, verbose_name="Returned")

    class Meta:
        ordering = ['-borrow_date']
        verbose_name = "Borrowing"
        verbose_name_plural = "Borrowings"

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if not self.returned:
            return timezone.now() > self.due_date
        return False

    @property
    def remaining_days(self):
        if not self.returned:
            delta = self.due_date - timezone.now()
            return max(delta.days, 0)
        return 0


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Student")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Book")
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Rating")
    comment = models.TextField(blank=True, verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Review Date")

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created_at']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"


class Contact(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=300, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class VisitLog(models.Model):
    path = models.CharField(max_length=500, verbose_name="URL Path")
    method = models.CharField(max_length=10, verbose_name="HTTP Method")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Visit Log"
        verbose_name_plural = "Visit Logs"

    def __str__(self):
        return f"{self.path} - {self.timestamp}"
