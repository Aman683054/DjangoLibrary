from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Book, Review
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from random import  randint
from django.template import RequestContext

# Create your views here.
def index(request):
    request.session.set_test_cookie()
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})

# def test_cookie(request):
#     if not request.COOKIES.get('number'):
#         response = HttpResponse("Cookie Set")
#         response.set_cookie('number', str(randint(1, 100)))
#         return response
#     else:
#         return HttpResponse(request.COOKIES['number'])


def about(request):
    # if request.session.test_cookie_worked():
    #     print("Cookies worked")
    #     request.session.delete_test_cookie()
    response = HttpResponse(render(context = None))
    context = RequestContext(request)

    if request.COOKIES['number']:
        number = request.COOKIES['number']
    else:
        number = response.set_cookie('number', randint(1, 100))
    # value = request.COOKIES['number']
    return render(request, 'myapp/about.html', {'value': number})


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'myapp/detail.html', {'book': book})


def findbooks(request):
    CATEGORY_CHOICES = {
        'S': 'Science&Tech',
        'F': 'Fiction',
        'B': 'Biography',
        'T': 'Travel',
        'O': 'Other'
    }
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            if (category):
                booklist = Book.objects.filter(category=category, price__lte=max_price)
                return render(request, 'myapp/results.html',
                              {'booklist': booklist, 'name': name, 'category': CATEGORY_CHOICES[category]})
            else:
                booklist = Book.objects.filter(price__lte=max_price)
                return render(request, 'myapp/results.html', {'booklist': booklist, 'name': name})

        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            books = form.cleaned_data['books']
            # book = order.books
            # order = form.save(commit=False)
            member = order.member
            total = 0
            for b in books:
                total += b.price
            # order.total_price = total
            type = order.order_type
            order.save()
            form.save_m2m()
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)

            return render(request, 'myapp/order_response.html', {'books': books, 'order': order, 'total': total})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if rating <= 5 and rating >= 1:
                reviews = form.save(commit=False)
                books = reviews.book
                books.num_reviews += 1
                books.save()
                reviews.save()
                return redirect('myapp:index')
            else:
                RatingErr = "You must enter a rating between 1 and 5!"
                return render(request, 'myapp/review.html', {'form': form, 'RatingErr': RatingErr})
        else:
            return HttpResponse('Please fill the form correctly')

    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            sign_up = form.save(commit=False)
            sign_up.password = make_password(form.cleaned_data['password'])
            sign_up.save()
            return index(request)
        else:
            HttpResponse("Please fill all the fields correctly")
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def chk_reviews(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        total = 0
        avg_review = 0
        ratings = Review.objects.filter(book__id=book_id)
        if ratings:
            for r in ratings:
                rate = r.rating
                total += rate
            total_no_of_reviews = Book.objects.get(id=book_id).num_reviews
            avg_review = total/total_no_of_reviews
            return render(request, 'myapp/chk_reviews.html', {'book': book, 'avg_review': avg_review})
        else:
            Rating_err = "There are no reveiws as of now"
            return render(request, 'myapp/chk_reviews.html', {'book': book, 'Rating_Err': Rating_err })
    else:
        return HttpResponse("You are not a registered Client")