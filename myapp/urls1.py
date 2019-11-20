from django.urls import path
from myapp import views1

app_name = 'myapp'

urlpatterns = [
    path(r'', views1.index, name='index'),
    path(r'about', views1.about, name='about'),
    path(r'order', views1.order, name='order'),
    path(r'<book_id>', views1.detail, name='detail'),

    ]
