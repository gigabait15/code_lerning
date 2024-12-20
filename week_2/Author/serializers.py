from rest_framework import serializers

from Author.models import Author
from Book.serializers import BookTitleSerializer


class AuthorSerializer(serializers.ModelSerializer):
    """
    Серилизатор для модели автора
    Поле books используется для передачи названия книги данного автора
    """
    books = BookTitleSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'books']