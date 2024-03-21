from django.shortcuts import render, redirect
from .models import Book, ViewBook
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def add_books(request):
    if request.method == 'GET':
        books = Book.objects.filter(user = request.user)
        views_totals = ViewBook.objects.filter(book__user = request.user).count()
        return render(
            request, 'add_books.html',{'books': books,'views_totals':views_totals}
        )
    elif request.method == 'POST':
        title = request.POST.get('titulo')
        file = request.FILES['arquivo']

        book = Book(user=request.user, title=title, file=file)
        book.save()
        messages.add_message(
            request, constants.SUCCESS, 'Apostila adicionada com sucesso.'
        )
        return redirect('/books/add_books/')

def book(request, id):
    book = Book.objects.get(id=id)

    view = ViewBook(
    ip=request.META['REMOTE_ADDR'],
    book=book
    )
    view.save()

    views_unics = ViewBook.objects.filter(book=book).values('ip').distinct().count()
    views_totals = ViewBook.objects.filter(book=book).count()

    return render(request, 'book.html', {'book': book, 'views_unics':views_unics, 'views_totals': views_totals})