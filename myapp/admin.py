from django.contrib import admin
from django.contrib import admin
from django.db.models import F
from .models import Publisher, Book, Order, Member, Review

admin.site.register(Order)
admin.site.register(Member)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'rating', 'reviewer')


admin.site.register(Review, ReviewAdmin)


# Register your models here.

def UpdatePriceBy10(modeladmin, request, queryset):
    queryset.update(price = F('price') + 10)


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price')
    actions = [UpdatePriceBy10]


admin.site.register(Book, BookAdmin)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'city')


admin.site.register(Publisher, PublisherAdmin)
