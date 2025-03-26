from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
import uvicorn
from fastapi import FastAPI, HTTPException
import json
import os
from pydantic import BaseModel, validator
from typing import Optional, List
from sqlalchemy import func
from sqlalchemy import and_
import logging


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


     # Определение отношения к User_book
    user_books = relationship("User_book", back_populates="book")
    # Опционально: Прямое отношение к User через User_book
    users = relationship("User", secondary="users_book", back_populates="books")    

# Таблица пользователей
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    is_active = Column(Integer, default=1)
    email = Column(String, unique=True)

    # Определение отношения к User_book
    user_books = relationship("User_book", back_populates="user")
    # Опционально: Прямое отношение к Book через User_book
    books = relationship("Book", secondary="users_book", back_populates="users")    


# Таблица пользователей
class User_book(Base):
    __tablename__ = 'users_book'
    
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    id_book = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    sum_book = Column(Integer)

    # Определение отношений к User и Book
    user = relationship("User", back_populates="user_books")
    book = relationship("Book", back_populates="user_books")    



# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Инициализация базы данных
Base.metadata.create_all(engine)


@app.get("/book_users/{book_id}")
async def get_book_users(book_id: int):
    """Получить всех пользователей, которые взяли конкретную книгу"""
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Книга с id {book_id} не найдена")
    
    # Использование отношения для получения пользователей
    return {"book": book.title, "users": [{"id": ub.user.id, "name": ub.user.name} for ub in book.user_books]}



@app.get("/user_book")
async def get_user_book():
    """Получение списка пользователей с их книгами"""
    users_books = session.query(User_book).all()
    return users_books


@app.post("/extra_book")
async def get_extra_books(id_book: int, id_user: int):
    """Выдача книг пользователю"""

    user = session.query(User).filter(User.id == id_user).first()
    book = session.query(Book).filter(Book.id == id_book).first()


    if not user:
        raise HTTPException(status_code=404, detail=f" Пользователь с id {id_user}  не существует")
    if not book:
        raise HTTPException(status_code=404, detail=f" Книга с id {id_book} не существует")
    if not user.is_active:
        raise HTTPException(status_code=404, detail="Данный пользователь не активирован")

    user_book = session.query(User_book).filter(User_book.id_user == id_user, User_book.id_book == id_book).first()
    if user_book:
        raise HTTPException(status_code=409, detail=f"Пользователь {id_user} уже взял {id_book} книгу")
    
    
    db_user_book = User_book( id_user=id_user, id_book=id_book, sum_book=1 )
    
    session.add(db_user_book)
    session.commit()

    
    return {"message": f"Книга {book.title} id={id_book} выдана пользователю {user.name} id={id_user}, ", "success": True}
    # return {"book": book.title, "users": [{"id": ub.user.id, "name": ub.user.name} 
    #                                      for ub in book.user_books]}



@app.post("/users")
async def create_user(name: str, fullname: str, email: str):
    """Создание нового пользователя"""
    existing_user = session.query(User).filter(User.name == name, User.fullname == fullname).first()
    if existing_user:
        raise HTTPException(status_code=409, detail=f"Пользователь с {name} и {fullname} существует ")
     
    email_user = session.query(User).filter(User.email == email).first()
    if email_user:
        raise HTTPException(status_code=409, detail=f"Пользователь с таким {email} существует ")

    db_user = User(
        name=name,
        fullname=fullname,
        email=email
      )

    session.add(db_user)
    session.commit()
    return {"message": "Пользователь успешно создан", "success": True}


@app.get("/show_users")
async def show_users():
    """Вывод списка пользователей"""
    all_users = session.query(User).all()
    return all_users


@app.put("/activate_user")
async def activate_user(user_id: int):
    """Активация пользователя"""
    existing_user = session.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не существует ")
    

    
    if existing_user.is_active == 1:
        raise HTTPException(status_code=400, detail=f"Пользователь {user_id} уже активирован")

    
    existing_user.is_active = 1

    session.commit()

    return {"message": "Пользователь успешно активирован", "success": True}


@app.put("/deactivate_user")
async def deactivate_user(user_id: int):
    """Деактивация пользователя"""
    existing_user = session.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не существует ")
    

    
    if existing_user.is_active == 0:
        raise HTTPException(status_code=400, detail=f"Пользователь {user_id} уже деактивирован")

    
    existing_user.is_active = 0

    session.commit()

    return {"message": "Пользователь успешно деактивирован", "success": True}


@app.get("/show_user")
async def show_user(name: str = None, fullname: str = None, user_id: str = None):
    """Получение информации о пользователе"""
    if user_id:
        existing_user = session.query(User).filter(User.id == user_id).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не существует ")
        return existing_user

    if name and fullname:
        existing_user = session.query(User).filter(User.name == name, User.fullname == fullname).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail=f"Пользователь {name} {fullname} не существует ")
        return existing_user

    raise HTTPException(status_code=400, detail="Не указан ID или имя и фамилия пользователя")



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
    """Удаление книги по id"""
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    


    
    session.delete(book)
    session.commit()
    return {"message": "Книга успешна удалена", "success": True}



@app.get("/show_book")
async def show_book(title: str, author: str,):
    """Поиск книги по title, author"""
    book = session.query(Book).filter(Book.title == title, Book.author == author).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    return book

@app.get("/multiple_books")
async def multiple_books(book_id: int = None, title: str = None, author: str = None, genre: str = None, year: int = None, rating: int = None):
    """Поиск книги по id, title, author, genre, year, rating""" 

    filters = []

    if book_id:
        filters.append(Book.id == book_id)
    if title:
        filters.append(Book.title == title)
    if author:
        filters.append(Book.author == author)
    if genre:
        filters.append(Book.genre == genre)
    if year:
        filters.append(Book.year == year)
    if rating:
        filters.append(Book.rating == rating)

    if filters:
            book = session.query(Book).filter(and_(*filters)).all()
    else:
            book = session.query(Book).all()

    if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена")

    return book

    


@app.put("/edit_book")
async def edit_book(book_id: int, title: str = None, author: str = None, genre: str = None, year: int = None, rating: int = None):
    """Редактирование книг"""


    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")




    if title:
        book.title = title
    if  author:
         book.author = author
    if genre:
        book.genre = genre
    if year:
        book.year = year
    if rating:
        book.rating = rating

        
    
    

    session.commit()
    return {"message": "Книга успешно изменена", "success": True}
 

@app.get("/library_stats")
async def library_stats():
    """Статистика библиотеки"""
    all_book = session.query(Book).all()
    if not all_book:
        raise HTTPException(status_code=404, detail="Книги не найдены")

    total_books = session.query(func.count(Book.id)).scalar()  
    avg_rating = round(session.query(func.avg(Book.rating)).scalar(), 2)
    avg_year = round(session.query(func.avg(Book.year)).scalar(), 2)
    
        
    return {"Общее количество книг": total_books, "Средний рейтинг": avg_rating, "Средний год ": avg_year}





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