FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y curl netcat-openbsd iputils-ping && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]