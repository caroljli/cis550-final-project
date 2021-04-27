from django.db import models

# Create your models here.

class Book(models.Model):
    bookID = models.IntegerField()
    title = models.CharField(max_length=100)
    
    # authors = models.CharField(max_length=900)
    # average_rating = models.IntegerField()
    # isbn = models.IntegerField()
    # isbn13 = models.IntegerField()
    # language_code = models.CharField(max_length=100)
    # num_pages = models.IntegerField()
    # ratings_count = models.IntegerField()
    # text_reviews_count = models.IntegerField()
    # publication_date = models.DateField()
    # publisher = models.CharField(max_length=100)
    