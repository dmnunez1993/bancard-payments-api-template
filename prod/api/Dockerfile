FROM python:3.10-alpine

RUN apk add postgresql-libs gcc musl-dev postgresql-dev

RUN mkdir /backend

# Setup code
COPY ./backend/requirements.txt /backend/requirements.txt
WORKDIR /backend

RUN pip install -r requirements.txt

COPY ./backend/. /backend/

# Set up pythonpath
ENV PYTHONPATH=/backend

CMD ["python3", "cmd/api.py"]
