FROM python:3.10-slim

RUN apt-get update && apt-get install -y graphviz && apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]
