FROM python:3.14 AS build
RUN pip install mysqlclient

FROM python:3.14-slim

WORKDIR /app

COPY --from=build /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
RUN apt-get update && apt-get install -y libmariadb3

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 9001

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py loaddata initial_data.json && python manage.py runserver 0.0.0.0:9001"]
