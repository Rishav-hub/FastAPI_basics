from fastapi import FastAPI
from enum import Enum
app = FastAPI()


BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}


class DirectionName(str, Enum):
    north = 'north'
    south = 'south'
    east = 'east'
    west = 'west'





@app.get("/")
async def read_all_books():
    return BOOKS


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {
            'Direction': direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {
            'Direction': direction_name, "sub": "Down"}
    if direction_name == DirectionName.east:
        return {
            'Direction': direction_name, "sub": "Left"}
    return {'Direction': direction_name, "sub": "Right"}



@app.get("/books/mybook")
async def read_favourite_book():
    return {"book_title": "My favourite book is..."}

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {"book_title": book_id}