FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY src/ ./src/

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV PYTHONPATH=/app/src

WORKDIR /app/src
RUN flask db migrate -m "Initial migration." && flask db upgrade

CMD ["flask", "run", "--host=0.0.0.0"]