from django.shortcuts import get_object_or_404, render, redirect
import json
from django.http import JsonResponse
from .models import Book, Todo
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import TodoSerializer

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_todos(request):
    try:
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    except Exception as e:
        # Log the exception for debugging
        print("Error in todo_list view:", e)
        return Response({"error": "An internal server error occurred."}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_todo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            book_title = data.get('book_title')
            todo_title = data.get('todo_title')

            if book_id and todo_title:
                try:
                    book = Book.objects.get(id=book_id)
                    
                except Book.DoesNotExist:
                    book = None

                todo = Todo.objects.create(book=book, todo_title=todo_title, user=request.user)

                logger.debug(f"Todo created for book {book.title} by user {request.user}")

                return JsonResponse({
                    'id': todo.id, 
                    'todo_title': todo_title, 
                    'book': book_title, 
                    'completed': todo.completed
                })
            
        except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error processing request: {e}")
                return JsonResponse({'error': 'Invalid JSON data or missing fields'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo(request, todo_id):
    if request.method == 'DELETE':
        try:
            todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
            todo.delete()
            return Response({'message': 'Todo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Todo.DoesNotExist:
            logger.error(f"Todo with ID {todo_id} does not exist.")
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in delete_todo view: {e}")
            logger.error(f"Error processing request: {e}")
            return Response({'error': 'An error occurred while deleting the todo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_todo(request, todo_id):
    try:
        todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
        todo.completed = not todo.completed
        todo.save()
        return Response({'message': 'Todo updated successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return Response({'error': 'An error occurred while updating the todo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)