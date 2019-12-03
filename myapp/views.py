import pytz
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect, reverse, render_to_response
from django.template.loader import render_to_string
from datetime import datetime
from .models import Book, Review, Member
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from random import  randint
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext

# Create your views here.
def index(request):
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = "Your last login was more than one hour ago!!"
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist, 'last_login': last_login})


def about(request):

    if 'number' in request.COOKIES:
        mynum = request.COOKIES['number']
        fav_number = render(request, 'myapp/about.html', {'mynum': mynum})
    else:
        mynum = randint(1, 100)
        fav_number = render(request, 'myapp/about.html', {'mynum': mynum})
        fav_number.set_cookie('number', mynum, 30)
    return fav_number
    # return  render(request, 'myapp/about.html')


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

@login_required
def place_order(request):
    try:
        if Member.objects.get(id=request.user.id):
            if request.method == 'POST':
                form = OrderForm(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    books = form.cleaned_data['books']
                    # book = order.books
                    # order = form.save(commit=False)
                    # member = order.member
                    member = Member.objects.get(id=request.user.id)
                    order.member = member
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
    except Member.DoesNotExist:
        Member_err = "You are not a registered client"
        return render(request, 'myapp/placeorder.html', {'Member_err': Member_err})


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
        form = RegisterForm(request.POST, request.FILES)
        valid_format = ['jpg', 'png', 'jpeg']
        if form.is_valid():
            print("Hi")
            image = form.cleaned_data['avatar']
            img = str(image).split('.')
            # print(img)
            if img[1] in valid_format:

                sign_up = form.save(commit=False)
                sign_up.password = make_password(form.cleaned_data['password'])
                sign_up.save()

                return index(request)
            else:

                Message_Err= "Wrong image format"
                return render(request, 'myapp/register.html', {'form': form, 'Message_Err': Message_Err})
        else:
            Message_Err = "Please fill all the fields correctly"
            return render(request, 'myapp/register.html', {'form': form, 'Message_Err': Message_Err})
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form})


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        current_login_time = datetime.now(pytz.timezone('America/Toronto'))
        timestamp = current_login_time.strftime("%d-%b-%Y (%H:%M:%S)")
        request.session['last_login'] = 'Last Login: ' + timestamp
        request.session.set_expiry(3600)
        if user:
            if user.is_active:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return HttpResponseRedirect(reverse(('myapp:index')))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            # return HttpResponse('Invalid login details.')
            Member_err = "Please enter the details correctly"
            return render(request, 'myapp/login.html', {'Member_err': Member_err})
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))

@login_required
def chk_reviews(request, book_id):
    try:
        if Member.objects.get(id=request.user.id):
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
                Rating_err = "There are no reviews as of now"
                return render(request, 'myapp/chk_reviews.html', {'book': book, 'Rating_Err': Rating_err })
        # else:
        #     return HttpResponse("You are not a registered Client")
    except Member.DoesNotExist:
        Member_err = "You are not a registered client"
        return render(request, 'myapp/chk_reviews.html', {'Member_err': Member_err})

