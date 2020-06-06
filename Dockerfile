FROM python:3.7.7
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt
ADD backend .
EXPOSE 8080
CMD ["uwsgi", "--ini", "/app/wsgi.ini"]
