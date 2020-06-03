FROM python:3.7.7-alpine3.10
RUN apk add --virtual .build-dependencies \
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            pcre-dev
RUN apk add --no-cache pcre
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk del .build-dependencies && rm -rf /var/cache/apk/* && rm requirements.txt
COPY manvsvirus-2944b63208f8.json .
ADD backend .
EXPOSE 80
CMD ["uwsgi", "--ini", "/app/wsgi.ini"]