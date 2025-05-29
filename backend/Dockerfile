FROM python:3.11-slim

WORKDIR /app

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/backend

ENV FLASK_APP=backend
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run"]
