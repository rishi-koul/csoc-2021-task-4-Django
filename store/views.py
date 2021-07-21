from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    num_available = 0
    context['book'] = Book.objects.get(id=bid)
    book_title = Book.objects.get(id=bid).title
    for book in BookCopy.objects.all():
        if(book.book.title == book_title):
            if book.borrower is None:
                num_available+=1
    context['num_available'] = num_available

    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE

    books_list = []
    for book in Book.objects.all():
        if get_data:
            if (book.title.startswith(get_data['title']) and 
                book.author.startswith(get_data['author']) and 
                book.genre.startswith(get_data['genre'])):
                books_list.append(book)
        else:
            books_list.append(book)

    context['books'] = books_list
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    
    username = request.user.username

    books_list = []
    for bookCpy in BookCopy.objects.all():
        if bookCpy.borrower != None:
            if bookCpy.borrower.username == username:
                books_list.append(bookCpy)

    context['books'] = books_list
    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = int(request.POST['bid'])# get the book id from post data

    book_title = Book.objects.get(id=book_id).title
    done = False
    for bookCpy in BookCopy.objects.all():
        if bookCpy.book.title == book_title and bookCpy.borrower is None:
            response_data['message'] = 'success'
            bookCpy.borrower = request.user
            bookCpy.save()
            done = True
            break
    if not done:
        response_data['message'] = 'failure'

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    response_data = {
        'message': 'failure',
    }
    book_id = int(request.POST['bid'])
    book = BookCopy.objects.get(id=book_id)

    book.borrower = None
    response_data['message'] = 'success'
    book.save()

    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBookView(request):
    
    response_data = {
        'message': None,
    }
    book_id = int(request.POST['bid'])
    book_rating = float(request.POST['rating'])
    book = Book.objects.get(id=book_id)

    if(Ratings.objects.filter(user=request.user, book=book).exists()):
        print("I do exist")
        prev_rating = Ratings.objects.get(user=request.user, book=book)
        print("\nUser: ", request.user.username, " Store: ", prev_rating.prev_rating, "\n")
        book.rating = ((book.rating * len(Ratings.objects.filter(book=book))) - prev_rating.prev_rating + book_rating)/len(Ratings.objects.filter(book=book))
        prev_rating.prev_rating = book_rating
        prev_rating.save()
    else:
        print("I do not exist")
        temp_book_rating = (book.rating * len(Ratings.objects.filter(book=book)))
        Ratings.objects.create(user=request.user, book=book, prev_rating= 0.0).save()
        book.rating = (temp_book_rating + book_rating)/len(Ratings.objects.filter(book=book))
        prev_rating = Ratings.objects.get(user=request.user, book=book)
        prev_rating.prev_rating = book_rating
        prev_rating.save()
    
    book.save()
    response_data['message'] = 'success'

    return JsonResponse(response_data)