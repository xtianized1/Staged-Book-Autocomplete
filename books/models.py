from django.db import models
from django.contrib.auth.models import User

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
    
class Meeting(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    meeting_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return f"Meeting for {self.book.title} on {self.meeting_date}"

class Note(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Note by {self.user.username} on {self.book.title}"