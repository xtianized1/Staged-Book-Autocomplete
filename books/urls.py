from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_search, name='book_search'),
    path('todos/', views.create_todo, name='create_todo'),
    path('user-todos/', views.user_todos, name='user_todos'),
    path('delete-todos/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('mark-todos/<int:todo_id>/', views.mark_todo, name='mark_todo'),
]