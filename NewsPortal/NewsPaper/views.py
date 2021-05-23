from datetime import datetime, timezone

from django.shortcuts import render

# импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView

# импортируем модель Product из models.py
from .models import Post


# создадим модель объектов, которые будем выводить
# Используется ListView - определяет список объектов, которые хотим отобразить.
# По умолчанию это просто даст нам все для модели, которую мы указали.
# Переопределив этот метод, мы можем расширить или полностью заменить эту логику.
class PostsList(ListView):
    # в данном случае рассматриваются все посты,
    # поэтому model = Post из файла models.py
    model = Post  # в нашем случае модель - Post (статья/новость)

    # зададим шаблон странички, в данном случае файл news.html
    # если не задать, то django автоматически выведет это имя из названия модели
    # и получится newspaper/post_list.html, которая всё-равно будет находится в папке templates
    # template_name = 'news.html'

    # также, можно указать название шаблона в поле context_object_name,
    # либо не указывать, тогда newspaper/post_list.html будет выбран по умолчанию, как шаблон
    # context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_qty'] = len(Post.objects.all())
        return context

    # сортируем все обекты модели Post по параметру даты создания в обратном порядке:
    def get_queryset(self):
        qset = super().get_queryset()
        return qset.order_by('-id', '-date_created')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
