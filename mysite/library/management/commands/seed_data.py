"""
Management command to seed the database with realistic test data.
Creates authors, categories, books, a test student, and sample reviews.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library.models import Author, Category, Book, UserProfile, Borrowing, Review
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed database with realistic library data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # --- Create Categories ---
        categories_data = [
            {'name': 'Fiction', 'icon': 'fas fa-feather-alt'},
            {'name': 'Science', 'icon': 'fas fa-flask'},
            {'name': 'Technology', 'icon': 'fas fa-laptop-code'},
            {'name': 'History', 'icon': 'fas fa-landmark'},
            {'name': 'Philosophy', 'icon': 'fas fa-brain'},
            {'name': 'Biography', 'icon': 'fas fa-user-tie'},
            {'name': 'Self-Help', 'icon': 'fas fa-hands-helping'},
            {'name': 'Mathematics', 'icon': 'fas fa-calculator'},
        ]
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'  Created category: {cat.name}')

        # --- Create Authors ---
        authors_data = [
            {'name': 'George Orwell', 'bio': 'Eric Arthur Blair, known by his pen name George Orwell, was an English novelist, essayist, journalist, and critic. His work is characterised by lucid prose, social criticism, opposition to totalitarianism, and support of democratic socialism.'},
            {'name': 'J.K. Rowling', 'bio': 'Joanne Rowling, better known by her pen name J. K. Rowling, is a British author and philanthropist. She wrote Harry Potter, a seven-volume fantasy series published from 1997 to 2007.'},
            {'name': 'Stephen Hawking', 'bio': 'Stephen William Hawking was an English theoretical physicist, cosmologist, and author who was director of research at the Centre for Theoretical Cosmology at the University of Cambridge.'},
            {'name': 'Robert C. Martin', 'bio': 'Robert Cecil Martin, known as Uncle Bob, is an American software engineer, instructor, and author. He is most recognized for developing many software design principles and for being a founder of Agile software development.'},
            {'name': 'Yuval Noah Harari', 'bio': 'Yuval Noah Harari is an Israeli public intellectual, historian and professor in the Department of History at the Hebrew University of Jerusalem.'},
            {'name': 'Malcolm Gladwell', 'bio': 'Malcolm Timothy Gladwell is a Canadian journalist, author, and public speaker. He has been a staff writer for The New Yorker since 1996.'},
            {'name': 'Marcus Aurelius', 'bio': 'Marcus Aurelius Antoninus was Roman emperor from 161 to 180 AD and a Stoic philosopher. He was the last of the rulers known as the Five Good Emperors.'},
            {'name': 'Walter Isaacson', 'bio': 'Walter Seff Isaacson is an American writer and journalist. He is the University Professor of History at Tulane University, and has been the President and CEO of the Aspen Institute.'},
        ]
        authors = {}
        for auth_data in authors_data:
            author, created = Author.objects.get_or_create(name=auth_data['name'], defaults=auth_data)
            authors[auth_data['name']] = author
            if created:
                self.stdout.write(f'  Created author: {author.name}')

        # --- Create Books ---
        books_data = [
            {
                'title': '1984',
                'author': authors['George Orwell'],
                'category': categories['Fiction'],
                'description': 'A dystopian novel set in a totalitarian society ruled by Big Brother. The story follows Winston Smith as he secretly rebels against the oppressive regime through a forbidden love affair and quest for truth and freedom.',
                'publication_year': 1949,
                'pages': 328,
                'language': 'English',
                'total_copies': 5,
                'available_copies': 3,
            },
            {
                'title': 'Animal Farm',
                'author': authors['George Orwell'],
                'category': categories['Fiction'],
                'description': 'A satirical allegorical novella reflecting events leading to the Russian Revolution of 1917 and the Stalinist era of the Soviet Union. Orwell wrote it as a fable about the dangers of totalitarianism.',
                'publication_year': 1945,
                'pages': 112,
                'language': 'English',
                'total_copies': 4,
                'available_copies': 4,
            },
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'author': authors['J.K. Rowling'],
                'category': categories['Fiction'],
                'description': 'The first novel in the Harry Potter series. It follows Harry Potter, a young wizard who discovers his magical heritage on his eleventh birthday, when he receives a letter of acceptance to Hogwarts School of Witchcraft and Wizardry.',
                'publication_year': 1997,
                'pages': 223,
                'language': 'English',
                'total_copies': 6,
                'available_copies': 4,
            },
            {
                'title': 'Harry Potter and the Chamber of Secrets',
                'author': authors['J.K. Rowling'],
                'category': categories['Fiction'],
                'description': 'The second novel in the Harry Potter series. The plot follows Harry\'s second year at Hogwarts, during which a series of messages on the walls of the school corridors warn that the Chamber of Secrets has been opened.',
                'publication_year': 1998,
                'pages': 251,
                'language': 'English',
                'total_copies': 4,
                'available_copies': 3,
            },
            {
                'title': 'A Brief History of Time',
                'author': authors['Stephen Hawking'],
                'category': categories['Science'],
                'description': 'A landmark volume in science writing by one of the great minds of our time. Hawking attempts to explain a range of subjects in cosmology, including the Big Bang, black holes, and light cones.',
                'publication_year': 1988,
                'pages': 256,
                'language': 'English',
                'total_copies': 3,
                'available_copies': 2,
            },
            {
                'title': 'The Universe in a Nutshell',
                'author': authors['Stephen Hawking'],
                'category': categories['Science'],
                'description': 'Stephen Hawking brings us to the cutting edge of theoretical physics, exploring extra dimensions, time travel, and the quest for a unified theory of the universe.',
                'publication_year': 2001,
                'pages': 224,
                'language': 'English',
                'total_copies': 2,
                'available_copies': 2,
            },
            {
                'title': 'Clean Code',
                'author': authors['Robert C. Martin'],
                'category': categories['Technology'],
                'description': 'A handbook of agile software craftsmanship. Even bad code can function, but if code isn\'t clean, it can bring a development organization to its knees. This book teaches the practices and principles of clean code.',
                'publication_year': 2008,
                'pages': 464,
                'language': 'English',
                'total_copies': 5,
                'available_copies': 3,
            },
            {
                'title': 'The Clean Coder',
                'author': authors['Robert C. Martin'],
                'category': categories['Technology'],
                'description': 'A code of conduct for professional programmers. This book is packed with practical advice about everything from estimating and coding to refactoring and testing.',
                'publication_year': 2011,
                'pages': 256,
                'language': 'English',
                'total_copies': 3,
                'available_copies': 3,
            },
            {
                'title': 'Sapiens: A Brief History of Humankind',
                'author': authors['Yuval Noah Harari'],
                'category': categories['History'],
                'description': 'A narrative of humanity\'s creation and evolution that explores how biology and history have defined us and enhanced our understanding of what it means to be human.',
                'publication_year': 2011,
                'pages': 443,
                'language': 'English',
                'total_copies': 4,
                'available_copies': 2,
            },
            {
                'title': 'Homo Deus: A Brief History of Tomorrow',
                'author': authors['Yuval Noah Harari'],
                'category': categories['History'],
                'description': 'Yuval Noah Harari envisions a near future in which we face a new set of challenges. Homo Deus explores the projects, dreams and nightmares that will shape the twenty-first century.',
                'publication_year': 2015,
                'pages': 448,
                'language': 'English',
                'total_copies': 3,
                'available_copies': 3,
            },
            {
                'title': 'Outliers: The Story of Success',
                'author': authors['Malcolm Gladwell'],
                'category': categories['Self-Help'],
                'description': 'In this stunning book, Malcolm Gladwell takes us on an intellectual journey through the world of outliers—the best and the brightest, the most famous and the most successful.',
                'publication_year': 2008,
                'pages': 309,
                'language': 'English',
                'total_copies': 3,
                'available_copies': 2,
            },
            {
                'title': 'The Tipping Point',
                'author': authors['Malcolm Gladwell'],
                'category': categories['Self-Help'],
                'description': 'The tipping point is that magic moment when an idea, trend, or social behavior crosses a threshold, tips, and spreads like wildfire. Gladwell explores and brilliantly illuminates this phenomenon.',
                'publication_year': 2000,
                'pages': 301,
                'language': 'English',
                'total_copies': 2,
                'available_copies': 1,
            },
            {
                'title': 'Meditations',
                'author': authors['Marcus Aurelius'],
                'category': categories['Philosophy'],
                'description': 'A series of personal writings by Marcus Aurelius, setting forth his ideas on Stoic philosophy. The book has been praised as a classic of philosophical literature and remains deeply relevant today.',
                'publication_year': 180,
                'pages': 254,
                'language': 'English',
                'total_copies': 3,
                'available_copies': 3,
            },
            {
                'title': 'Steve Jobs',
                'author': authors['Walter Isaacson'],
                'category': categories['Biography'],
                'description': 'The definitive biography of Steve Jobs, based on more than forty interviews with Jobs conducted over two years—as well as interviews with more than a hundred family members, friends, and colleagues.',
                'publication_year': 2011,
                'pages': 656,
                'language': 'English',
                'total_copies': 3,
                'available_copies': 2,
            },
            {
                'title': 'Einstein: His Life and Universe',
                'author': authors['Walter Isaacson'],
                'category': categories['Biography'],
                'description': 'Walter Isaacson\'s biography explores how an imaginative, impertinent patent clerk became the mind reader of the creator of the cosmos, the locksmith of the mysteries of the atom and the universe.',
                'publication_year': 2007,
                'pages': 675,
                'language': 'English',
                'total_copies': 2,
                'available_copies': 2,
            },
        ]

        books = []
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            books.append(book)
            if created:
                self.stdout.write(f'  Created book: {book.title}')

        # --- Create test student user ---
        if not User.objects.filter(username='student').exists():
            student = User.objects.create_user(
                username='student',
                email='student@example.com',
                password='student123',
                first_name='Ahmed',
                last_name='Al-Salem',
            )
            UserProfile.objects.create(user=student, phone='+1234567890')
            self.stdout.write('  Created test student: student / student123')

            # Create a borrowing for the student
            book1 = books[0]  # 1984
            borrowing = Borrowing.objects.create(
                user=student,
                book=book1,
                due_date=timezone.now() + timedelta(days=10),
            )
            book1.available_copies -= 1
            book1.save()
            self.stdout.write(f'  Created borrowing: {student.username} -> {book1.title}')

            # Create some reviews
            review_data = [
                {'book': books[0], 'rating': 5, 'comment': 'A masterpiece of dystopian fiction. Every page is gripping and thought-provoking. Highly recommended!'},
                {'book': books[2], 'rating': 5, 'comment': 'A magical journey that captivates readers of all ages. The wizarding world is absolutely enchanting.'},
                {'book': books[4], 'rating': 4, 'comment': 'Hawking makes complex cosmology accessible to everyone. A must-read for anyone curious about the universe.'},
                {'book': books[6], 'rating': 5, 'comment': 'Essential reading for every programmer. Changed the way I write code. Every developer should read this.'},
                {'book': books[8], 'rating': 4, 'comment': 'A fascinating overview of human history. Harari presents complex ideas in an engaging and accessible way.'},
            ]

            # Need to create borrowings first for the reviews to be valid
            for review in review_data:
                if not Borrowing.objects.filter(user=student, book=review['book']).exists():
                    Borrowing.objects.create(
                        user=student,
                        book=review['book'],
                        due_date=timezone.now() - timedelta(days=5),
                        returned=True,
                        return_date=timezone.now() - timedelta(days=7),
                    )
                Review.objects.create(
                    user=student,
                    book=review['book'],
                    rating=review['rating'],
                    comment=review['comment'],
                )
                self.stdout.write(f'  Created review for: {review["book"].title}')

        # --- Create admin superuser ---
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write('  Created admin user: admin / admin123')

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('Test accounts:'))
        self.stdout.write(self.style.SUCCESS('  Student: username=student, password=student123'))
        self.stdout.write(self.style.SUCCESS('  Admin:   username=admin, password=admin123'))
