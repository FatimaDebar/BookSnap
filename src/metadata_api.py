import requests

def fetch_book_metadata(title, author=None):
    # Build the query string
    query = f"intitle:{title}"
    if author:
        query += f"+inauthor:{author}"
    
    # Construct the API URL
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    # Send the request
    response = requests.get(url)
    data = response.json()

    # Parse the response
    if 'items' in data:
        book = data['items'][0]['volumeInfo']
        return {
            'title': book.get('title'),
            'authors': book.get('authors'),
            'description': book.get('description'),
            'categories': book.get('categories'),
            'publishedDate': book.get('publishedDate'),
            'pageCount': book.get('pageCount'),
            'language': book.get('language')
        }
    else:
        return {'error': 'Book not found'}
result = fetch_book_metadata("The Great Gatsby", "F. Scott Fitzgerald")
print(result)
