from django.shortcuts import render, redirect
from books.models import Book

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
    books = Book.objects.all()
    print(books.count)
    return render(request, "book_directory.html", {"books": books})