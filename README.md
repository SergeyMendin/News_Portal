### Модуль D4.2.
GET-параметры в действии & django_filter & Paginator

Добавим страницу /news/search.
На ней должна быть реализована возможность пользователя искать новости по определённым критериям.
Критерии должны быть следующие:
позже какой-либо даты; 
по названию; 
по имени пользователя автора; 
всё вместе.
django_filter 
Действия: 
Установка пакета:
python -m pip install django-filter.
в файле settings.py, чтобы получить доступ к фильтрам в приложении добавляется в INSTALLED_APPS добавляем строку:
‘django_filters’
в папке, где находится models.py создется файл search.py;
в файле search.py пишем:
# импортируем filterset
from django_filters import FilterSet
# импортируем модель Post
from .models import Post
# создаём фильтр по указанным выше критериям
class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           # позже даты создания
           'date_created': ['gt'],

           # по названию
           'title': ['icontains'],

           # по автору
           'post_author': ['exact'],
           }
в файле views.py добавляем в модель PostLists:
# импортируем наш фильтр
from .search import PostFilter

# пишем модуль, который принимает на вход отфильтрованные объекты
def get_context_data(self, **kwargs):
   # распаковываем self = Posts
   context = super().get_context_data(**kwargs)
   context['search'] = PostFilter(
       self.request.GET,
       queryset=self.get_queryset()
   )
   return context


Добавьте постраничный вывод на основной странице новостей, чтобы на одной странице было не больше 10 новостей, и были видны номера лишь ближайших страниц, а также возможность перехода к первой или последней странице.
в html=шаблоне основной страниц добавим:
<!-- Перед таблицей добавим форму для поиска -->
<form method="GET">
   {{ search.form }} <!-- Форму от фильтров за нас сделает django.
   А вот кнопку, увы придётся делать самому -->
   <input type="submit" value="Найти">
</form>

для того, чтобы фильтр работал, перед выводом атрибутов модели post
добавляем строку:
{% for post in search.qs %} <!-- итерация фильтра -> search.qs передает отфильтрованные post-ы -->
чтобы были видны номера ближайших страниц, в конце шаблона добавляем:
<div class="pagination">
   <span class="step-links">
       {% if page_obj.has_previous %}
           <a href="?page=1">&laquo; Начало </a>
           <a href="?page={{ page_obj.previous_page_number }}"> <<< </a>
       {% endif %}

       <span class="current">
           Стр {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}.
       </span>

       {% if page_obj.has_next %}
           <a href="?page={{ page_obj.next_page_number }}"> >>> </a>
           <a href="?page={{ page_obj.paginator.num_pages }}"> Конец &raquo;</a>
       {% endif %}
   </span>
</div>

Paginator
Действия:
в модель, которая сделана на основе дженерика ListView, добавляем строку:
# установим постраничный вывод на каждую новость
paginate_by = 10
