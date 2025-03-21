from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import uvicorn
from fastapi import FastAPI, HTTPException
import json
import os
from pydantic import BaseModel, validator
from typing import Optional, List



app = FastAPI()

# Создание подключения к базе данных
engine = create_engine('postgresql://admin:1234@localhost:5432/library')


# Создание базового класса для моделей (новый стиль SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# Пример определения модели
class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    year = Column(Integer)
    rating = Column(Integer)



# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()


@app.get("/show_books")
async def show_books():
    """Вывод списка книг"""
    all_books = session.query(Book).all()
    return all_books  
    

@app.post("/add_book/")
async def add_book(
    title: str,
    author: str,
    genre: str,
    year: int,
    rating: int
):
    """Добавление книги"""
    existing_book = session.query(Book).filter(Book.title == title).first()
    if existing_book:
        raise HTTPException(status_code=409, detail="Книга с таким названием уже существует")
    
   

    db_book = Book(
        title= title,
        author= author,
        genre= genre,
        year= year,
        rating= rating
      )

    session.add(db_book)
    session.commit()
    return {"message": "Книга успешно добавлена", "success": True}



@app.delete("/remove_book/")
async def remove_book(book_id: int):
    """Удаление книги"""
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    


    
    session.delete(book)
    session.commit()
    return {"message": "Все книги успешно удалены", "success": True}



@app.get("/show_book")
async def show_book(title: str, author: str,):
    """Поиск одной книги"""
    book = session.query(Book).filter(Book.title == title, Book.author == author).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    return book
    




 






# # Создание базового класса для моделей
# Base = declarative_base()

# Добавление данных
# books = [
#     Book(title="Война и мир", author="Лев Толстой", genre="Роман", year=1869, rating=5),
#     Book(title="Гарри Поттер и философский камень", author="Дж. К. Роулинг", genre="Фэнтези", year=1997, rating=4)
# ]

# Добавление книг в сессию
# session.add_all(books)

# # Сохранение изменений
# session.commit()



# --------------------------------Способ получения всех значений--------------------------
# # Получить все книги
# all_books = session.query(Book).all()

# # Перебор всех книг
# for book in all_books:
#     print(f"{book.id}: {book.title} - {book.author} ({book.year})")


# # Получить книгу с ID = 1
# book = session.query(Book).get(1)
# # или более современный вариант в SQLAlchemy 2.0


#----------------------- Получить по id"--------------------------------------------------------
# book = session.get(Book, 1)

# if book:
#     print(f"{book.title} by {book.author}")
# else:
#     print("Книга не найдена")

# # Получить книги с рейтингом 5
# top_books = session.query(Book).filter(Book.rating == 5).all()

# # Получить книги определенного автора
# tolstoy_books = session.query(Book).filter(Book.author == "Лев Толстой").all()

# # Получить книги, написанные после 1900 года
# modern_books = session.query(Book).filter(Book.year < 1900).all()
# if not modern_books:
#     print("Нет книг, написанных после 1900 года")
#     print(modern_books)
# else:
#     print("Книга найдена")
#     print(modern_books)
#     print(len(modern_books))
#     for book in modern_books:
#         print(f"{book.title} - {book.author} ({book.year})")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)