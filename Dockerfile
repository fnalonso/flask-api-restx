FROM python:3.7.7-alpine

RUN addgroup -S app && adduser -S app -G app

RUN mkdir /opt/api
WORKDIR /opt/api

ADD . .
RUN pip install -r requirements.txt
RUN chown app.app -R /opt/api


EXPOSE 5000

ENTRYPOINT ["gunicorn", "--chdir", "src", "app:create_app()", "-b", "0.0.0.0:5000", "-w", "4", "--reload"]
