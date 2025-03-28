# import logging

# # # Настройка базового логгера
# # logging.basicConfig(
# #     level=logging.DEBUG,
# #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# #     filename='app.log', # Имя файла для записи логов 
# #     filemode='w', # Режим записи: 'w' - перезаписать, 'a' - дописать (append)
# # )

# # # Создание логгера
# # logger = logging.getLogger(__name__)

# # # Использование логгера
# # logger.debug("Это отладочное сообщение")
# # logger.info("Это информационное сообщение")
# # logger.warning("Это предупреждение")
# # logger.error("Это сообщение об ошибке")

import logging
from pythonjsonlogger import jsonlogger

# Создаем логгер
logger = logging.getLogger()

# Создаем обработчик для вывода в консоль
# handler = logging.StreamHandler()
handler = logging.FileHandler('app.log', encoding='utf-8')

# Создаем JSON форматтер
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s', json_ensure_ascii=False)

# Устанавливаем форматтер для обработчика
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Использование
logger.info("Это информационное сообщение")
logger.warning("Это предупреждение")
logger.error("Это сообщение об ошибке")

