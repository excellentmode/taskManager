# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/backend

ENV FLASK_APP=backend
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run"]
