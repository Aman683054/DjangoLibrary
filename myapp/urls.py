from django.urls import path
from myapp import views
from myapp.views import IndexView, detailView, MyPasswordResetView, MyPasswordResetDoneView, MyPasswordResetConfirmView, \
    MyPasswordResetCompleteView, MyChangePasswordView, MyChangePasswordConfirmView
from django.contrib.auth.urls import views as auth_views
app_name = 'myapp'

urlpatterns = [
    # path(r'', views.index, name='index'),
    path(r'', IndexView.as_view(), name='index'),
    path(r'about', views.about, name='about'),
    path(r'<int:pk>', detailView.as_view(), name='detail'),
    # path(r'<int:book_id>', views.detail, name='detail'),
    path(r'findbooks', views.findbooks, name='findbooks'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'myorders', views.Myorders, name='myorders'),
    path(r'review', views.review, name='review'),
    path(r'register', views.register, name='register'),
    path(r'login', views.user_login, name='login'),
    path(r'chk_reviews/<int:book_id>', views.chk_reviews, name='chk_reviews'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path(r'password_reset/done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(r'reset/done/', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path(r'password_change/', MyChangePasswordView.as_view(), name='password_change'),
    path(r'password_change/done/', MyChangePasswordConfirmView.as_view(), name='password_change_done'),

    ]
