## 🔴 Критические проблемы


1. **Инициализация базы данных**:
   - Отсутствует вызов `Base.metadata.create_all(engine)`. Если таблицы не существуют, приложение завершится с ошибкой. До этого все у нас было, куда-то затер)

## 🟠 Проблемы с API-дизайном

1. **Эндпоинт `/edit_book`**:
   - Используется GET-запрос для изменения данных. По принципам REST следует использовать PUT или PATCH.
   - ```python
     @app.get("/edit_book")  # Должно быть @app.put или @app.patch
     ```

2. **Эндпоинт `/remove_book/`**:
   - Сообщение об успехе неверное: `"Все книги успешно удалены"`, хотя удаляется только одна книга.

3. **Эндпоинт `/multiple_books`**:
   - Логическая ошибка: проверяется только один параметр (первый в цепочке if), даже если переданы несколько.
   - Для параметра `author` возвращается только первая книга (`.first()`), а не все а в других запросах все, не понятно что функция делает в итоге где-то у нас first где-то all.