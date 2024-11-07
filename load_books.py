import os
import sys
import django
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
import json
from books.models import Book

with open('books.json', 'r') as file:
    data = json.load(file)
    for item in data:
        book = Book(title=item['title'])
        book.save()
    print('Books loaded successfully!')
if __name__ == "__main__":
    insert_data()