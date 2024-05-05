FROM python:3.12.2-slim

WORKDIR /map

COPY requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /map

CMD ["python", "app.py"]