"""FastAPI Fields, POST, GET, PUT, DELETE"""


from wsgiref import headers
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length = 1, title="The title of the book")
    author: str = Field(min_length = 1, max_length= 100)
    description: Optional[str] = Field(max_length= 100,
                        min_length = 1,
                        title="The description of the book")
    rating: int = Field(gt= -1, lt= 101, default=0, title= "The rating of the book")

    class Config:
        schema_extra ={
            "example": {
                "id": "b1d8f6e0-e9e0-4e6e-b8e7-c9d8f7f9e7b1",
                "title": "The title of the book",
                "author": "RDash",
                "description": "The description of the book",
                "rating" : 122           
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length = 1, title="The title of the book")
    author: str = Field(min_length = 1, max_length= 100)
    description: Optional[str] = Field(max_length= 100,
                        min_length = 1,
                        title="The description of the book")
    

BOOKS = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):

    """Custom HTTPException handler
    """
    return JSONResponse(status_code=418,
                        content={"message": f"Hey, why do you want {exception.books_to_return} books?"
                                            "Enter a valid number of books to return!! Thanks"})

@app.post("/books/login")
async def book_login(username: str= Form(...), password: str= Form(...)):

    """Forms fields for user authentication and return a form to the backend"""
    return {"username": username, "password": password}

@app.get('/header')
async def read_header(random_header: Optional[str]= Header(None)):
    return {"Random-Header": random_header}

@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):

    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return = books_to_return)
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i<= books_to_return:
            new_books.append(BOOKS[i-1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise raise_item_cannot_be_found_exception()

@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    """New class with response model without raing
    """
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise raise_item_cannot_be_found_exception()

@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    """Custom Status code using status module"""
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for book_item in BOOKS:
        counter += 1
        if book_item.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception() 

@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for book_item in BOOKS:
        counter += 1
        if book_item.id == book_id:
            BOOKS.pop(counter - 1)
            return {"message": f"Book with ID:{book_id} deleted"}
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id= "5d2dd6c8-af83-49b9-895a-8d97b84688bb",
                  title= "Title 1",
                  author= "Author 1",
                  description= "Description 1",
                  rating= 60)
    book_2 = Book(id= "cf625e2f-3cef-4b70-a19b-c361179ec9f0",
                  title= "Title 2",
                  author= "Author 2",
                  description= "Description 2",
                  rating= 70)
    book_3 = Book(id= "5bac0187-8661-4b1f-aad8-f6f5b6b0de7d",
                  title= "Title 3",
                  author= "Author 3",
                  description= "Description 3",
                  rating= 80)
    book_4 = Book(id= "4390051d-288a-49fe-98bf-bc77c4e592dd",
                  title= "Title 4",
                  author= "Author 4",
                  description= "Description 4",
                  rating= 10)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)

def raise_item_cannot_be_found_exception():
    raise HTTPException(status_code=404, detail="Book not found",
                        headers= {"X-Header-Error": "Nothing to be seen at UUID"})
