from rest_framework import viewsets

from .models import Author
from Author.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet модели автора
    http_method_names указаны какие запросы будут использованы
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post', 'put']

    def list(self, request, *args, **kwargs):
        """GET /api/authors - возвращает список авторов"""
        return super(AuthorViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST /api/authors - создаёт нового автора"""
        return super(AuthorViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """PUT /api/authors/{id} - редактирует автора"""
        return super(AuthorViewSet, self).update(request, *args, **kwargs)