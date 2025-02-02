from flask import Flask,request,jsonify
app = Flask(__name__)

# In-memory storage for our books
books = [
    {"id": 1, "title":"The Great Gatsby", "author":"F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
]

# GET all books

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"book" : books})

#GET a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_id(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({"Error" : "Book not found 404"}), 404
    return jsonify({"book":book})

#POST a new book
@app.route('/books', methods=['POST'])
def create_book():
    if not request.is_json:
        return jsonify({"Error" : "Content-Type must be application/json"}), 400
    
    data = request.get_json();

     # Validate required fields
    if not all(key in data for key in ('title', 'author')):
        return jsonify({'message' : 'Missing title or author'}), 400
    
    # Generate new ID
    new_id = max(book['id'] for book in books) + 1

    new_book = {
        'id': new_id,
        'title':data['title'],
        'author':data['author'],
    }

    books.append(new_book)

    return jsonify({'book': new_book}), 201

#PUT update a book 
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if not request.is_json:
        return jsonify({"Error" : "Content-Type must be application/json"}), 400
    
    book = next((book for book in books if book['id']  == book_id ), None)
    if book is None:
        return jsonify({'Error': "Book not found"}),404
    
    data = request.get_json()

    # Update book details
    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])

    return jsonify({'book': book})

#DELETE a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    initial_length = len(books)

    books = [book for book in books if book['id'] != book_id]

    if len(books) == initial_length:
        return jsonify({'Error': 'Book not found'}), 404
    
    return jsonify({'message': 'book deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)