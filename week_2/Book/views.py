from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from Book.models import Book
from Book.serializers import BookSerializer


class PaginationPage(PageNumberPagination):
    """
    Класс для создания пагинации
    """
    page_size = 10
    page_size_query_param = 'page_size'


class BookViewSet(ModelViewSet):
    """
    ViewSet для модели класса книг
    в поле queryset добавлен order_by для сортировки по названию книг
    pagination_class используется для пагинации книг на странице
    filter_backends используется для фильтрации книг, данные для фильтрации указаны в search_fields
    http_method_names указаны какие запросы будут использованы
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    pagination_class = PaginationPage
    filter_backends = (filters.SearchFilter,)
    search_fields = ['author__first_name']
    http_method_names = ['get', 'post', 'put']

    # Описание полей с фильтрацией , пагинацией и выбором страницы
    @swagger_auto_schema(
        operation_description="GET /api/books - возвращает список книг",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Фильтрация книг по имени автора",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Номер страницы",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Количество книг на странице",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super(BookViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        POST /api/books - создает новую книгу
        Добавлена логика проверки наличия книг, если книга уже имеется добавляет количество книг переданное в запросе
        """
        title = request.data.get('title')
        author_id = request.data.get('author_id')
        count = request.data.get('count', 1)

        book = Book.objects.filter(title=title, author_id=author_id).first()

        if book:
            book.count += count
            book.save()
            return Response(self.get_serializer(book).data, status=status.HTTP_200_OK)
        else:
            return super(BookViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """PUT /api/books/{id} - редактирует книгу"""
        return super(BookViewSet, self).update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='buy')
    def buy(self, request, *args, **kwargs):
        """
        POST /api/books/{id}/buy - апи для покупки книги
        Если книга в наличии, то уменьшает количество иначе выдает ошибку
        """
        book_id = kwargs.get('pk')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Книги нет"}, status=status.HTTP_404_NOT_FOUND)

        if book.count > 0:
            book.count -= 1
            book.save()
            return Response({"message": f"Количество оставшихся книг {book.count}"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Книги закончились"}, status=status.HTTP_400_BAD_REQUEST)




