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
      book_name = input("\nВведите название: ")
      if len(book_name) < 1:
       print("Название книги не может быть пустым.")
       continue
      author = input("\nВведите автора: ")
      if len(author) < 1:
          print("Автор не может быть пустым.")
          continue
      janr = input("\nВведите жанр: " )
      if len(janr) < 1:
         print("Жанр не может быть пустым.")
         continue
      year = input("\nВведите год издания: ")
      if len(year) < 1:
         print("Год издания не может быть пустым.")
         continue
      reiting = input("\nВведите рейтинг (1-5): ")
      if len(reiting) < 1:
         print("Рейтинг должен быть числом от 1 до 5.")
         continue
      zapytay = input("\nДобавить в списки (через запятую): ").split(",")
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
         
         print(f"\nКнига успешно добавлена с ID: {new_id}")
         break 
 
      

       
      
def show_books():
 """Показать все книги"""
 while True:
     print("\n===== ВСЕ КНИГИ В БИБЛИОТЕКЕ =====")
     for book_id, book in library["books"].items():
         print(f"\nID: {book_id} ") 
         print(f"\nНазвание: {book['title']}")
         print(f"\nАвтор: {book['author']}")
         print(f"\nЖанр: {book['genre']}")
         print(f"\nГод издания: {book['year']}")
         print(f"\nРейтинг: {book['rating']}")
         print(f"\nСписки: {', '.join(book['lists'])}")
         print("\n----------------------------------------")
         print(f"Всего книг в библиотеке {book_id} ")
     break        
    
    
    

def remove_book():
 """Удаление книги по ID"""
 while True:
     print("\n===== УДАЛЕНИЕ КНИГИ =======")
     book_id = input("Введите ID книги: ")
     if len(book_id) < 1:
         print("ID книги не может быть пустым.")
         continue
     if book_id in library["books"]:
         del library["books"][book_id]
         print(f"Книга с ID: {book_id} успешно удалена.")
     else:
         print(f"Книга с ID: {book_id} не найдена.")
     break


def edit_book():
 """Редактирование информации о книге"""
 while True:
    print("\n===== РЕДАКТИРОВАНИЕ КНИГИ =====")
    book_id = input("Введите ID книги: ")
    if len(book_id) < 1:
        print("ID книги не может быть пустым.")
        continue
    if book_id in library["books"]:
        print("Информация о книге:")
        print(f"\nID: {book_id}")
        print(f"\nНазвание: {library['books'][book_id]['title']}")
        print(f"\nАвтор: {library['books'][book_id]['author']}")
        print(f"\nЖанр: {library['books'][book_id]['genre']}")
        print(f"\nГод издания: {library['books'][book_id]['year']}")
        print(f"\nРейтинг: {library['books'][book_id]['rating']}")
        print(f"\nСписки: {', '.join(library['books'][book_id]['lists'])}")
        print("----------------------------------------")
        new_title = input("Новое название (если не изменяется, оставьте поле пустым): ")
        new_author = input("Новый автор (если не изменяется, оставьте поле пустым): ")
        new_genre = input("Новый жанр (если не изменяется, оставьте поле пустым): ")
        new_year = input("Новый год издания (если не изменяется, оставьте поле пустым): ")
        new_rating = input("Новый рейтинг (если не изменяется, оставьте поле пустым): ")
        new_lists = input("Новые списки (через запятую) (если не изменяются, оставьте поле пустым): ").split(",")
        if new_title:
            library["books"][book_id]["title"] = new_title
            print("Изменено: Название")
        if new_author:
            library["books"][book_id]["author"] = new_author
            print("Изменено: Автор")
        if new_genre:
            library["books"][book_id]["genre"] = new_genre
            print("Изменено: Жанр")
        if new_year:
            library["books"][book_id]["year"] = new_year
            print("Изменено: Год издания")
        if new_rating:
            library["books"][book_id]["rating"] = int(new_rating)
            print("Изменено: Рейтинг")
        if new_lists:
            library["books"][book_id]["lists"] = new_lists
            print("Изменено: Списки")
        break    



def search_books():
 """Поиск книг по заданным критериям"""
 while True:
    print("\n===== ПОИСК КНИГ =====")
    print("1. По названию")
    print("2. По автору")
    print("3. По жанру")
    print("4. По году издания")
    print("5. По рейтингу")
    print("6. По списку")
    print("0. Выйти")

    choice = input("Выберите критерий поиска (1-6): ")

    if choice not in ["1", "2", "3", "4", "5", "6", "0"]:
        print("Неверный ввод. Попробуйте еще раз.")
        continue
    if choice == "2":
      choice1 = input("Ведите автора: ")
      for book_id, book in library["books"].items():
          if choice1.lower() == book["author"].lower():
              print(f"\nID: {book_id}")
              print(f"\nНазвание: {book['title']}")
              print(f"\nАвтор: {book['author']}")
              print(f"\nЖанр: {book['genre']}")
              print(f"\nГод издания: {book['year']}")
              print(f"\nРейтинг: {book['rating']}")
              print(f"\nСписки: {', '.join(book['lists'])}")
              print("\n----------------------------------------")
    else:
       print("Таких критериев поиска нету")
    if choice == "1":
       choice1 = input("Введите название: ")
       for book_id, book in library["books"].items():
           if choice1.lower() == book["title"].lower():
              print(f"\nID: {book_id}")
              print(f"\nНазвание: {book['title']}")
              print(f"\nАвтор: {book['author']}")
              print(f"\nЖанр: {book['genre']}")
              print(f"\nГод издания: {book['year']}")
              print(f"\nРейтинг: {book['rating']}")
              print(f"\nСписки: {', '.join(book['lists'])}")
              print("\n----------------------------------------")
    else:
       print("Таких критериев поиска нету")          
    if choice == "3":
       choice1 = input("Введите жанр: ")
       for book_id, book in library["books"].items():
           if choice1.lower() == book["genre"].lower():
              print(f"\nID: {book_id}")
              print(f"\nНазвание: {book['title']}")
              print(f"\nАвтор: {book['author']}")
              print(f"\nЖанр: {book['genre']}")
              print(f"\nГод издания: {book['year']}")
              print(f"\nРейтинг: {book['rating']}")
              print(f"\nСписки: {', '.join(book['lists'])}")
              print("\n----------------------------------------")
    else:
       print("Таких критериев поиска нету")          
    if choice == "4":
       choice1 = input("Введите год издания: ")
       for book_id, book in library["books"].items():
           if int(choice1) == book["year"]:
              print(f"\nID: {book_id}")
              print(f"\nНазвание: {book['title']}")
              print(f"\nАвтор: {book['author']}")
              print(f"\nЖанр: {book['genre']}")
              print(f"\nГод издания: {book['year']}")
              print(f"\nРейтинг: {book['rating']}")
              print(f"\nСписки: {', '.join(book['lists'])}")
              print("\n----------------------------------------")
    else:
       print("Таких критериев поиска нету")
    if choice == "5":
       choice1 = input("Введите рейтинг: ")
       for book_id, book in library["books"].items():
           if int(choice1) == book["rating"]:
              print(f"\nID: {book_id}")
              print(f"\nНазвание: {book['title']}")
              print(f"\nАвтор: {book['author']}")
              print(f"\nЖанр: {book['genre']}")
              print(f"\nГод издания: {book['year']}")
              print(f"\nРейтинг: {book['rating']}")
              print(f"\nСписки: {', '.join(book['lists'])}")
              print("\n----------------------------------------")
    else:
       print("Таких критериев поиска нету")
    if choice == "6":
       choice1 = input("Введите списк: ")     
       for book_id, book in library["books"].items():
           if choice1.lower() == book["lists"]:
              print(f"\nID: {book_id}")
              print(f"\nНазвание: {book['title']}")
              print(f"\nАвтор: {book['author']}")
              print(f"\nЖанр: {book['genre']}")
              print(f"\nГод издания: {book['year']}")
              print(f"\nРейтинг: {book['rating']}")
              print(f"\nСписки: {', '.join(book['lists'])}")
              print("\n----------------------------------------")
              print(f"\nНайдено книг: {book_id}")
    else:
       print("Таких критериев поиска нету")
    if choice == "0":
       print("----------------------------------------")
       print("\nВы вышли из меню поиска книг")
       main_menu()
       

         
              
                                            
                    



def show_statistics():
 """Вывод статистики по библиотеке"""
 while True:
    print(f"\n===== СТАТИСТИКА БИБЛИОТЕКИ =====")
    print(f"\nОбщее количество книг: {len(library['books'])}")
    

           

          

    




def main_menu():
 """Основное меню программы"""

 while True:
     print("\n===== МЕНЕДЖЕР ЛИЧНОЙ БИБЛИОТЕКИ =====")
     print("\n1. Добавить новую книгу")
     print("2. Удалить книгу")
     print("3. Редактировать книгу")
     print("4. Поиск книг")
     print("5. Показать статистику")
     print("6. Показать все книги")
     print("0. Выход")
     choice = input("\nВведите номер опции: ")

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
     elif choice == "6":
        show_books()
     elif choice == "0":
        break
     else:
         print("Неверный ввод. Попробуйте снова.")

 





# Запуск программы
if __name__ == "__main__":
 library = load_library()
 main_menu()
