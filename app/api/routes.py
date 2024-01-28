from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, Library, lib_schema, libs_schema

api = Blueprint('api', __name__, url_prefix='/api')


# create books
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):    #reference in models
    book_type = request.json['book_type']
    author_first = request.json['author_first']
    author_last = request.json['author_last']
    title = request.json['title']
    book_len = request.json['book_len']
    isbn = request.json['isbn']
    user_token = current_user_token.token

    print(f'TESTER:  {current_user_token.token}')

    new_book = Library(book_type, author_first, author_last, title, book_len, isbn, user_token=user_token)  #order matters

    db.session.add(new_book)
    db.session.commit()

    response = lib_schema.dump(new_book)
    return jsonify(response)

# retrieve all books
@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Library.query.filter_by(user_token = a_user).all()
    response = libs_schema.dump(books)
    return jsonify(response)

# retrieve single book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Library.query.get(id) #retrieving from data base
    response = lib_schema.dump(book) #pulling it out
    return jsonify(response)

#update book info
@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book (current_user_token, id):
    book = Library.query.get(id)
    book.author_first = request.json['author_first']
    book.author_last = request.json['author_last']
    book.title = request.json['title']
    book.book_len = request.json['book_len']
    book.book_type = request.json['book_type']
    book.isbn = request.json['isbn']

    db.session.commit()
    response = lib_schema.dump(book)
    return jsonify(response)

#delete book
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Library.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = lib_schema.dump(book)
    return jsonify(response)


