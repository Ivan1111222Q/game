import uvicorn
from fastapi import FastAPI, HTTPException
import json
import os
from pydantic import BaseModel, validator
from typing import Optional, List


app = FastAPI()





@app.on_event("startup")
def startup_event():
    global library
    library = load_library()

def load_library(filename="library.json"):
    """
    Загружает библиотеку из JSON файла.
    
    Args:
        filename (str): Путь к файлу библиотеки
        
    Returns:
        dict: Словарь с данными библиотеки или пустую структуру, если файл не найден
    """
    # Базовая структура пустой библиотеки
    empty_library = {
        "books": {},
        "user_lists": ["Любимые", "Прочитано", "Хочу прочитать", "Классика"]
    }
    
    # Проверяем существование файла
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден. Создана новая библиотека.")
        return empty_library
    
    try:
        # Открываем и загружаем данные из файла
        with open(filename, 'r', encoding='utf-8') as file:
            library = json.load(file)
            print(f"Библиотека успешно загружена из {filename}")
            return library
    except json.JSONDecodeError as e:
        print(e) 
        print(f"Ошибка чтения файла {filename}. Создана новая библиотека.")
        return empty_library
    except Exception as e:
        print(f"Произошла ошибка при загрузке библиотеки: {e}")
        return empty_library
    


def save_library(library, filename="library.json"):
    """
    Сохраняет библиотеку в JSON файл.
    
    Args:
        library (dict): Словарь с данными библиотеки
        filename (str): Путь к файлу для сохранения
        
    Returns:
        bool: True если сохранение успешно, иначе False
    """
    try:
        # Открываем файл и записываем данные в формате JSON
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(library, file, ensure_ascii=False, indent=2)
            print(f"Библиотека успешно сохранена в файл '{filename}'")
            return True
    except Exception as e:
        print(f"Произошла ошибка при сохранении библиотеки: {e}")
        return False
    




@app.get("/show_books")
async def show_books():
    """Вывод списка книг"""
    return library
   

@app.delete("/remove_book/{book_id}")
async def remove_book(book_id: str):
    """Удаление книги"""
    if book_id in library["books"]:
        del library["books"][book_id]
        save_library(library)    
        return {"message": "Книга успешно удалена", "success": True}
    else:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    

@app.post("/add_book/{book_id}")
async def add_book(book_id: str, book_data: dict):
    """Добавление книги"""
    if book_id in library["books"]:
        raise HTTPException(status_code=409, detail="Книга с таким ID уже существует")
    library["books"][book_id] = book_data
    save_library(library)
    return {"message": "Книга успешно добавлена", "success": True}



@app.patch("/edit_book/{book_id}")
async def edit_book(book_id: str, book_data: dict):
    """Редактирование книги"""
    if book_id not in library["books"]:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    library["books"][book_id].update(book_data)
    save_library(library)
    return {"message": "Книга успешно изменена", "success": True}












if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)