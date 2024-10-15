from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_ratings = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comment_ratings = self.user.comment_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        post_comment_ratings = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum'] or 0
        self.rating = (post_ratings * 3) + comment_ratings + post_comment_ratings
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPE = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=ARTICLE)
    time_created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...' if len(self.content) > 124 else self.content

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


