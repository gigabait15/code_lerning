from django.urls.conf import path

from Book.views import BookViewSet


urlpatterns = [
    path('books/', BookViewSet.as_view({'get': 'list'}), name='book_list'),
    path('books/', BookViewSet.as_view({'post': 'create'}), name='book_create'),
    path('books/<int:pk>/', BookViewSet.as_view({'put': 'update'}), name='book_update'),
    path('books/<int:pk>/buy/', BookViewSet.as_view({'post': 'buy'}), name='book_buy'),
]