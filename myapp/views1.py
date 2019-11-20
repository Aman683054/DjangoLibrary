from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Publisher, Book, Member, Order

# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('id')[:10]
    publisherlist = Publisher.objects.all().order_by('-city')
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>'+ str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    heading2 = '<p>' + 'List of available publisher: ' + '</p>'
    response.write(heading2)
    for publisher in publisherlist:
        para = '<p>' + str(publisher.name) + ': ' + str(publisher.city) + '<p>'
        response.write(para)
    return response

def about(request):
    response = HttpResponse()
    response.write("This is an eBook APP")
    return response

def order(request):
    response = HttpResponse()
    order = Order.objects.get(id =4)
    for bk in order.total_items():

        response.write(str(bk) +"<br>")
    return response

def detail(request, book_id):
    response = HttpResponse()
    try:
        book = Book.objects.get(id = book_id)

        heading1 = '<table align="center"> <col width="300"><col width="300"><col width ="300">' + '<tr>' + '<th>' + 'Book Title' + '</th>' + '<th>' + '&nbsp &nbsp Book Price' + '</th>' + '<th>' + '&nbsp &nbsp Publisher' + '</th></table>'
        response.write(heading1)
        heading2 = '<table align="center" ><col width="400"><col width="320"> <td>' + str.upper(
            book.title) + '</td>' + '<td> &nbsp &nbsp $' + str(book.price) + '</td>' + '<td> &nbsp &nbsp' + str(
            book.publisher) + '</td> </tr> </table>'
        response.write(heading2)
        # response.write(order)

    except Book.DoesNotExist:
        response.write("Book not found")



    return response
