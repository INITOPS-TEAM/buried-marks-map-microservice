FROM python:3.14

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 9001

CMD ["sh", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 127.0.0.1:9001"]
