from rest_framework import serializers
from .models import Book, Todo

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']

class TodoSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    class Meta:
        model = Todo
        fields = ['id', 'book', 'todo_title', 'completed']

    def get_book(self, obj):
        if obj.book:
            return obj.book.title
        return None