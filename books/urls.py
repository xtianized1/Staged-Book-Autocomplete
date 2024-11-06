from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_search, name='book_search'),
    path('todos/', views.create_todo, name='create_todo'),
    path('todo_list/', views.todo_list, name='todo_list'),
]