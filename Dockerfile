#./Dockerfile
FROM python:3.8

WORKDIR /usr/src/app 

COPY requirements.txt ./ 

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000   

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]