from django.shortcuts import render, redirect
from books.models import Book
from books.models import BestBook

# logistical

def splash(request):
    # if request.user.is_authenticated:
    #     if Student.objects.filter(user=request.user).count() > 0:
    #         return redirect("/student_home")
    #     else:
    #         return redirect("/restaurant_home")
    # else:
	    # return render(request, "splash.html", {})
    return render(request, "splash.html", {})

def book_directory(request):
    search_params = request.GET.get("search_params")
    print(search_params)

    authors_params = request.GET.get("authors_params")
    print(authors_params)

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
    else: 
        results = Book.objects.all()
    return render(request, "book_directory.html", {"books": results}) 

def authors(request):
     results = BestBook.objects.raw('SELECT authors as ID FROM BESTSELLERS GROUP BY authors ORDER BY COUNT(authors) DESC FETCH first 10 rows only')
     return render(request, "authors.html", {"authors" : results})

def mostreviews(request):
     results = BestBook.objects.raw('SELECT DISTINCT b.title as ID FROM BESTSELLERS b ORDER BY b.reviews DESC FETCH FIRST 10 rows only')
     return render(request, "mostreviews.html", {"reviews" : results})