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
    search_params = request.GET.get("search_params")
    print(search_params)
    if search_params is not None:
        results = Book.objects.filter(title__icontains = search_params) | Book.objects.filter(authors__icontains = search_params)
    else: 
        results = Book.objects.all()
    return render(request, "book_directory.html", {"books": results})