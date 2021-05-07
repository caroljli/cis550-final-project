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

    # if authors_params:
    #     print("yes")
    #     results = BestBook.objects.all()
    #     return redirect("/authors.html", {"authors": results})


    if search_params is not None:
        results = Book.objects.filter(title__icontains = search_params) | Book.objects.filter(authors__icontains = search_params)
    # elif authors_params is not None:
    #     results = BestBook.objects.raw('SELECT b.name FROM BESTSELLERS b WHERE b.author = ${authors_params}')
    else: 
        results = Book.objects.all()
    return render(request, "book_directory.html", {"books": results}) 

def authors(request):
     results = BestBook.objects.raw('SELECT author as ID FROM BESTSELLERS GROUP BY author ORDER BY COUNT(author) DESC FETCH first 10 rows only')
     return render(request, "authors.html", {"authors" : results})