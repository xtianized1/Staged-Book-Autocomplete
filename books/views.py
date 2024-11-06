from django.shortcuts import get_object_or_404, render, redirect
import json
from django.http import JsonResponse
from .models import Book, Todo
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def book_search(request):
    query = request.GET.get('query', '')
    
    books_data = Book.objects.all()

    if query:
        books = [book for book in books_data if query.lower() in book.title.lower()]
        results = [{'id': book.id, 'title': book.title} for book in books]
    else:
        results = []
    
    return JsonResponse(results, safe=False)

def todo_list(request):
    todos = Todo.objects.all()
    todolist = [{
        'book': todo.book.title if todo.book else 'No Book',
        'todo_title': todo.todo_title,
        'completed': todo.completed
    } for todo in todos]
    
    return JsonResponse(todolist, safe=False)

@csrf_exempt
def create_todo(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        book_id = data.get('book_id')
        book_title = data.get('book_title')
        todo_title = data.get('todo_title')
        if book_id and todo_title:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                book = Book.objects.create(title=book_title)
                print("New Book added")
                
            todo = Todo.objects.create(book=book, todo_title=todo_title)
            
            logger.debug(f"Todo created for book {book.title} by user {request.user}")

            return JsonResponse({
                'id': todo.id, 
                'todo_title': todo_title, 
                'book': book_title, 
                'completed': todo.completed
            })
        
    return JsonResponse({'error': 'Invalid data'}, status=400)