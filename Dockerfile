FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "app.py"]
