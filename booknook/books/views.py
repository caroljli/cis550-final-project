from django.shortcuts import render, redirect
from books.models import Book, BestBook
from user.models import BookReview

# logistical

def book_directory(request):
    logged_in = True
    search_params = request.GET.get("search_params")
    print(search_params)

    authors_params = request.GET.get("authors_params")
    print(authors_params)

    genre_params = request.GET.get("genre_params")
    print(genre_params)

    # if authors_params:
    #     print("yes")
    #     results = BestBook.objects.all()
    #     return redirect("/authors.html", {"authors": results})

    results = Book.objects.all()
    if search_params is not None:
        results = Book.objects.filter(title__icontains = search_params) | Book.objects.filter(authors__icontains = search_params)
    elif authors_params is not None:
        param_dict = { "param": authors_params }
        results = BestBook.objects.raw('SELECT DISTINCT * FROM BESTSELLERS b WHERE b.authors = %(param)s', param_dict)
    elif genre_params is not None:
        param_dict = { "param": genre_params }
        results = BestBook.objects.raw('SELECT * FROM BESTSELLERS b WHERE b.genre = %(param)s ORDER BY b.rating DESC FETCH FIRST 10 rows only', param_dict)
    else: 
        results = Book.objects.all()
    return render(request, "book_directory.html", {"books": results, "logged_in": logged_in})

def book(request, url=None):
    logged_in = True
    if Book.objects.get(id=url):
        book = Book.objects.get(id=url)
        reviews = BookReview.objects.filter(book_title=url)
        return render(request, "book.html", {"book": book, "logged_in": logged_in, "reviews": reviews})
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
