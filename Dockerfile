FROM python:3.11-slim

# ffmpeg مطلوب من start.sh، وبعض الحزم تحتاج أدوات بناء
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh Run

CMD ["python3", "main.py"]
