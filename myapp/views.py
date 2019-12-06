import pytz
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404, redirect, reverse, render_to_response
from datetime import datetime
from .models import Book, Review, Member, User, Order
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from random import randint
from django.views.generic import ListView, DetailView
from django.contrib.auth.urls import views as auth_views


# Class based view
class IndexView(ListView):
    model = Book
    template_name = 'myapp/book_list.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if 'last_login' in self.request.session:
            context['last_login'] = self.request.session['last_login']
        else:
            context['last_login'] = "Your last login was more than one hour ago!!"
        return context


# Create your views here.
# def index(request):
#     if 'last_login' in request.session:
#         last_login = request.session['last_login']
#     else:
#         last_login = "Your last login was more than one hour ago!!"
#     booklist = Book.objects.all().order_by('id')[:10]
#     return render(request, 'myapp/index.html', {'booklist': booklist, 'last_login': last_login})


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


class detailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'

    def get_queryset(self):
        return Book.objects.filter(id=self.kwargs['pk'])


# def detail(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     return render(request, 'myapp/detail.html', {'book': book})


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

                    return render(request, 'myapp/order_response.html',
                                  {'books': books, 'order': order, 'total': total})
                else:
                    return render(request, 'myapp/placeorder.html', {'form': form})

            else:
                form = OrderForm()
                return render(request, 'myapp/placeorder.html', {'form': form})
    except Member.DoesNotExist:
        Member_err = "You are not a registered client"
        return render(request, 'myapp/placeorder.html', {'Member_err': Member_err})


@login_required
def review(request):
    try:
        if Member.objects.get(id=request.user.id, status__in=(1, 2)):
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    rating = form.cleaned_data['rating']
                    if rating <= 5 and rating >= 1:
                        reviews = form.save(commit=False)
                        books = reviews.book
                        books.num_reviews += 1
                        member = Member.objects.get(id=request.user.id)
                        reviews.reviewer = member.email
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
    except Member.DoesNotExist:
        Member_err = "You are not a registered client"
        return render(request, 'myapp/review.html', {'Member_err': Member_err})


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

                Message_Err = "Wrong image format"
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
                avg_review = total / total_no_of_reviews
                return render(request, 'myapp/chk_reviews.html', {'book': book, 'avg_review': avg_review})
            else:
                Rating_err = "There are no reviews as of now"
                return render(request, 'myapp/chk_reviews.html', {'book': book, 'Rating_Err': Rating_err})
        # else:
        #     return HttpResponse("You are not a registered Client")
    except Member.DoesNotExist:
        Member_err = "You are not a registered client"
        return render(request, 'myapp/chk_reviews.html', {'Member_err': Member_err})


class MyPasswordResetView(auth_views.PasswordResetView):
    template_name = 'myapp/password_reset_form.html'
    # email_template_name = 'registration/password_reset_email.html'
    # extra_email_context={'new_password': '123459876'}
    def form_valid(self, form):
        new_password = User.objects.make_random_password()
        user_email = form.cleaned_data['email']
        try:
            if User.objects.get(email=user_email):
                user = User.objects.get(email=user_email)
                user.set_password(new_password)
                user.save()
                self.extra_email_context = {'new_password': new_password}
                return super().form_valid(form)
        except User.DoesNotExist:
            message_err = "Please enter a valid email id that is registered"
            # self.extra_email_context = {'message_err': message_err}
            return render(self.request, 'myapp/password_reset_form.html', {'form':form, 'message_err': message_err})



class MyPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'myapp/password_reset_done.html'


class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'myapp/password_reset_confirm.html'


class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'myapp/password_reset_complete.html'

class MyChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'myapp/password_change_form.html'


class MyChangePasswordConfirmView(auth_views.PasswordChangeDoneView):
    template_name = 'myapp/password_change_done.html'


@login_required
def Myorders(request):
    try:
        if Member.objects.get(id=request.user.id):
            if Order.objects.filter(member__id=request.user.id):
                orderlist = Order.objects.filter(member__id=request.user.id)
                return render(request, 'myapp/myorders.html', {'orderlist':orderlist})
            else:
                Member_err = "You have no orders to display"
                return render(request, 'myapp/myorders.html', {'Member_err': Member_err})
    except Member.DoesNotExist:
        Member_err = "You are not a registered client"
        return render(request, 'myapp/myorders.html', {'Member_err': Member_err})


