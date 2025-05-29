FROM python:3.11-slim

WORKDIR /app

COPY backend /app/backend
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=backend

EXPOSE 5000

CMD ["flask", "run"]