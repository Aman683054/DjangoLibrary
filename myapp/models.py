from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from upload_validator import FileTypeValidator

from .validator import maxvaluevalidator, minvaluevalidator
from django.core.validators import FileExtensionValidator, validate_image_file_extension


# Create your models here--------------
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, default='USA')
    def __str__(self):
        return self.name


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[maxvaluevalidator, minvaluevalidator])
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

class Member(User):
    STATUS_CHOICES = {
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    }

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)
    avatar = models.FileField(upload_to='profile', help_text="Accepted format are .PNG, .JPEG, .JPG", blank=True, null=True)
    def books_borrowed(self):
        list1 = []
        for books in self.borrowed_books.all():
            list1.append(books.title)
        return list1



class Order(models.Model):
    ORDER_CHOICES = [
        (0, 'Purchase'),
        (1, 'Borrow')
    ]
    books = models.ManyToManyField(Book)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)
    # total_price = models.DecimalField(max_digits=10, decimal_places=2,  blank=True, null=True)
    def total_items(self):
        list1 = []
        for book in self.books.all():
            list1.append(book.title)
        return list1
    def total_books(self):
        return len(self.books.all())

    def __str__(self):
        return str(self.id) + " " + str(self.order_date)

class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.id) + " " + str(self.date)