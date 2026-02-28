FROM python:3.14

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

EXPOSE 9001

CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata initial_data.json && python manage.py runserver 0.0.0.0:9001"]
