import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Author Name')),
                ('bio', models.TextField(blank=True, verbose_name='Biography')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='authors/', verbose_name='Photo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Category Name')),
                ('icon', models.CharField(default='fas fa-book', max_length=50, verbose_name='Icon Class')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(max_length=300, verbose_name='Subject')),
                ('message', models.TextField(verbose_name='Message')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Contact Message',
                'verbose_name_plural': 'Contact Messages',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Book Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='books/', verbose_name='Cover Image')),
                ('publication_year', models.PositiveIntegerField(default=2024, verbose_name='Publication Year')),
                ('pages', models.PositiveIntegerField(default=0, verbose_name='Number of Pages')),
                ('language', models.CharField(default='English', max_length=50, verbose_name='Language')),
                ('total_copies', models.PositiveIntegerField(default=1, verbose_name='Total Copies')),
                ('available_copies', models.PositiveIntegerField(default=1, verbose_name='Available Copies')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library.author', verbose_name='Author')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='library.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateTimeField(auto_now_add=True, verbose_name='Borrow Date')),
                ('due_date', models.DateTimeField(verbose_name='Due Date')),
                ('return_date', models.DateTimeField(blank=True, null=True, verbose_name='Return Date')),
                ('returned', models.BooleanField(default=False, verbose_name='Returned')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowings', to='library.book', verbose_name='Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowings', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Borrowing',
                'verbose_name_plural': 'Borrowings',
                'ordering': ['-borrow_date'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Phone Number')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/', verbose_name='Profile Picture')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='VisitLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=500, verbose_name='URL Path')),
                ('method', models.CharField(max_length=10, verbose_name='HTTP Method')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP Address')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Visit Log',
                'verbose_name_plural': 'Visit Logs',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Rating')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Review Date')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='library.book', verbose_name='Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'book')},
            },
        ),
    ]
