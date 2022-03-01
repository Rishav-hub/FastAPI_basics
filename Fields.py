"""FastAPI Fields, POST, GET, PUT, DELETE"""


from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
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


BOOKS = []

@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):
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
    return {"error": "Book not found"}

@app.post('/')
async def create_book(book: Book):
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
        
@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for book_item in BOOKS:
        counter += 1
        if book_item.id == book_id:
            BOOKS.pop(counter - 1)
            return {"message": f"Book with ID:{book_id} deleted"}
    return {"error": "Book not found"}


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



