from rest_framework import serializers
from Book.models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Серилизатор для модели книг
    """
    class Meta:
        model = Book
        fields = '__all__'


class BookTitleSerializer(serializers.ModelSerializer):
    """
    Серилизатор для модели книг, который используется в серилизаторе автора для передачи названия
    """
    class Meta:
        model = Book
        fields = ['title']


