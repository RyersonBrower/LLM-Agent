FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY utils.py .
COPY knowledge/ ./knowledge/


CMD ["python", "app.py"]
