FROM python:3.7.7-alpine

RUN mkdir /opt/api

WORKDIR /opt/api

ADD . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--chdir", "src", "app:app", "-b", "0.0.0.0:5000", "-w", "4", "--reload"]
