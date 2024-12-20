from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author.Author', related_name='books', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

