from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Todo(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    todo_title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.todo_title} (Book: {self.book.title})"