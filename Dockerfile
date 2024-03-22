FROM python:3.12.2-alpine

RUN apk update && apk add git

WORKDIR /usr/src/app

RUN git clone --branch main --single-branch --depth 1 https://github.com/greywidget/notify.git .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./.env .

COPY ./startup.sh .

CMD ["./startup.sh"]
