FROM python:3.11-slim

WORKDIR /apptivity

RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-db.sh /wait-for-db.sh

RUN chmod +x /wait-for-db.sh

RUN chown root:root /wait-for-db.sh

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]