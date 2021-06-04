# импортируем библиотеку для работы с путями urls
from django.urls import path
# импортируем наше представление
from .views import PostsList, PostDetailedView, PostCreateView
from . import views

urlpatterns = [
    path('', PostsList.as_view()),

    # детали поста
    path('<int:pk>/', PostDetailedView.as_view(), name='post_details'),
    # создание поста
    path('<int:pk>/', PostCreateView.as_view(), name='post_create'),




]