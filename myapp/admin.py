import decimal

from django.contrib import admin
from django.contrib import admin
from django.db.models import F
from .models import Publisher, Book, Order, Member, Review
from django.contrib import messages

admin.site.register(Member)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'rating', 'reviewer')


admin.site.register(Review, ReviewAdmin)


# Register your models here.

def UpdatePriceBy10(modeladmin, request, queryset):
    for book in queryset:
        if book.price <= 990:
            # queryset.update(price = F('price') + 10)
            book.price = book.price + decimal.Decimal('10')
            book.save()
            messages.success(request, "Successfully updated book '" + book.title + "'")
        else:
            messages.error(request,"Price getting more than 1000 in book '" + book.title + "'")
    UpdatePriceBy10.short_description = "Adding 10 to price"


class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('id', 'title', 'category', 'price')
    actions = [UpdatePriceBy10]


admin.site.register(Book, BookAdmin)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'city')


admin.site.register(Publisher, PublisherAdmin)

class OrderAdmin(admin.ModelAdmin):
    fields = [('books'),('member', 'order_type','order_date')]
    list_display = ('id', 'member', 'order_type','order_date', 'total_books')


admin.site.register(Order, OrderAdmin)
