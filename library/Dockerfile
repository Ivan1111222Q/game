FROM python:3.12.8

WORKDIR /app

# 1. Копируем только requirements.txt
COPY requirements.txt .

# 2. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем остальной код (после установки зависимостей)
COPY . .

CMD [ "python", "main.py" ]
