import json
import os


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



def add_book():
 """Добавление новой книги"""
 print("\n===== ДОБАВЛЕНИЕ НОВОЙ КНИГИ =====")
 while True:
      book_name = input("Введите название: ")
      if len(book_name) < 1:
       print("Название книги не может быть пустым.")
       continue
      author = input("Введите автора: ")
      if len(author) < 1:
          print("Автор не может быть пустым.")
          continue
      janr = input("Введите жанр: " )
      if len(janr) < 1:
         print("Жанр не может быть пустым.")
         continue
      year = input("Введите год издания: ")
      if len(year) < 1:
         print("Год издания не может быть пустым.")
         continue
      reiting = input("Введите рейтинг (1-5): ")
      if len(reiting) < 1:
         print("Рейтинг должен быть числом от 1 до 5.")
         continue
      zapytay = input("Добавить в списки (через запятую): ").split(",")
      for book_id, book in library["books"].items():
         if any(zapytay_item.lower() == book["title"].lower() for zapytay_item in zapytay):
            print(f"Книга '{book_name}' уже есть в списках: {', '.join(zapytay)}")
            continue
         
      
         
      if book_name  not in library["books"]:
         max_id = max(int(book_id) for book_id in library["books"].keys())
         new_id = str(max_id + 1) 
         library["books"][new_id] = {
              "title": book_name,
              "author": author,
              "genre": janr,
              "year": year,
              "rating": int(reiting),
              "lists": zapytay
          }
         
         print(f"Книга успешно добавлена с ID: {new_id}")
         break 
 
      

       
      
        
    
    
    

     



 

def remove_book():
 """Удаление книги по ID"""
 pass


def edit_book():
 """Редактирование информации о книге"""
 pass

def search_books():
 """Поиск книг по заданным критериям"""
 pass


def show_statistics():
 """Вывод статистики по библиотеке"""
 pass


def main_menu():
 """Основное меню программы"""

 while True:
     print("\nМеню библиотеки:")
     print("1. Добавить новую книгу")
     print("2. Удалить книгу по ID")
     print("3. Редактировать информацию о книге")
     print("4. Поиск книг по заданным критериям")
     print("5. Вывод статистики по библиотеке")
     print("0. Выход")
     choice = input("Введите номер опции: ")

     if choice == "1":
         add_book()
     elif choice == "2":
         remove_book()
     elif choice == "3":
         edit_book()
     elif choice == "4":
        search_books()
     elif choice == "5":
        show_statistics()
     elif choice == "0":
        break
     else:
         print("Неверный ввод. Попробуйте снова.")

 


# Запуск программы
if __name__ == "__main__":
 library = load_library()
 main_menu()
