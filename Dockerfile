#downloads lghtweight linux image
FROM python:3.13-slim  

#every command now runs in app folder
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#this application listens on port 8000
EXPOSE 8000

#uvicorn app.main:app --host 0.0.0.0 --port 8000 (write this to start container)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]