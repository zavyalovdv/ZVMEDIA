FROM python:3.14-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN adduser -D zvmedia

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY . .

RUN chown -R zvmedia:zvmedia /app

USER zvmedia

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "-k", "gthread", "--workers", "4", "--threads", "4", "--bind", "0.0.0.0:8000", "ZVMEDIA.wsgi:application"]