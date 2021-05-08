from django.db import models

# Create your models here.

class Book(models.Model):
    ID = models.IntegerField()
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=800)
    rating = models.IntegerField()
    class Meta:
        db_table = "BOOKS_EXTENSIVE"
    
class BestBook(models.Model):
    ID = models.IntegerField()
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=900)
    rating = models.IntegerField()
    class Meta:
        db_table = "BESTSELLERS"
    
    
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

# class BookNookUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     bio = models.TextField()
#     time = models.DateTimeField(auto_now=True, null=True)
#     # following = models.ManyToManyField(Follow, related_name='following', null=True)
#     picture = models.CharField(max_length=600, null=True)