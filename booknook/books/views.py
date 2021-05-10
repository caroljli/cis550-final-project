from django.shortcuts import render, redirect
from books.models import Book, BestBook, BookFollowers
from user.models import BookReview, BookNookUser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

# logistical

def splash(request):
    return render(request, "splash.html", {})

def book_directory(request):
    logged_in = True
    search_params = request.GET.get("search_params")
    print(search_params)

    authors_params = request.GET.get("authors_params")
    print(authors_params)

    genre_params = request.GET.get("genre_params")
    print(genre_params)

    year_params = request.GET.get("year_params")

    recommended_params = request.GET.get("recommended_params")

    results = Book.objects.all()
    if search_params is not None:
        results = Book.objects.filter(title__icontains = search_params) | Book.objects.filter(authors__icontains = search_params)
    elif authors_params is not None:
        param_dict = { "param": authors_params }
        results = BestBook.objects.raw('SELECT DISTINCT * FROM BESTSELLERS b WHERE b.authors = %(param)s', param_dict)
    elif genre_params is not None:
        param_dict = { "param": genre_params }
        results = BestBook.objects.raw('SELECT DISTINCT b.title, b.ID, b.authors, b.rating FROM BESTSELLERS b WHERE b.genre = %(param)s ORDER BY b.rating DESC FETCH FIRST 10 rows only', param_dict)
    elif year_params is not None:
        param_dict = { "param": year_params }
        results = BestBook.objects.raw('SELECT DISTINCT b.title, b.ID, b.authors, b.rating FROM BESTSELLERS b WHERE b.year >= %(param)s', param_dict)
    elif recommended_params is not None:
        param_dict = { "param": recommended_params }
        book = BestBook.objects.raw('SELECT * FROM BESTSELLERS WHERE b.title =  %(param)s FETCH FIRST 1 rows only', param_dict)

        results = BestBook.objects.raw('SELECT b.title FROM BESTSELLERS b WHERE b.rating < %(param)s', param_dict) 
    else: 
        results = Book.objects.all()
    return render(request, "book_directory.html", {"books": results, "logged_in": logged_in})

def book(request, url=None):
    logged_in = True
    followers = BookFollowers.objects.filter(ID=url)
    try: 
        followers.get(follower_id=request.user.id)
        followed = True
    except ObjectDoesNotExist:
        followed = False
    if Book.objects.get(id=url):
        book = Book.objects.get(id=url)
        reviews = BookReview.objects.filter(book_title=url)
        return render(request, "book.html", {"book": book, "logged_in": logged_in, "reviews": reviews, "followed": followed})
    else:
        return render("404: book not found")

def authors(request):
    logged_in = True
    results = BestBook.objects.raw('SELECT authors as ID FROM BESTSELLERS GROUP BY authors ORDER BY COUNT(authors) DESC FETCH first 10 rows only')
    return render(request, "authors.html", {"authors" : results, "logged_in": logged_in})

def mostreviews(request):
    logged_in = True
    results = BestBook.objects.raw('SELECT DISTINCT b.title as ID FROM BESTSELLERS b ORDER BY b.reviews DESC FETCH FIRST 10 rows only')
    return render(request, "mostreviews.html", {"reviews" : results, "logged_in": logged_in})

def topreviewers(request):
    logged_in = True
    results = BookReview.objects.raw('SELECT author_name as ID from BOOKREVIEW GROUP BY (author_name) ORDER BY (author_name) ASC FETCH FIRST 10 ROWS ONLY')
    return render(request, "topreviewers.html", {"reviewers" : results, "logged_in": logged_in})

def follow_book(request):
    print(request.POST.get('follow_book'))
    print(request.user.id)

    user = request.user
    bnfollower = BookNookUser.objects.filter(ID=user.id).first()
    if 'follow_book' in request.POST:
        to_follow = Book.objects.get(ID=request.POST.get('follow_book'))
        BookFollowers.objects.create(ID=to_follow.ID, title=to_follow.title, follower_id=bnfollower.ID, follower_name=bnfollower.name)
        print(bnfollower.name)
    else:
        BookFollowers.objects.filter(ID=request.POST.get('unfollow_book')).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))