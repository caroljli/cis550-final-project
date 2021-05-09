from django.contrib import admin
from user.models import BookNookUser, BookReview, UserFollowers

admin.site.register(BookNookUser)
admin.site.register(BookReview)
admin.site.register(UserFollowers)
