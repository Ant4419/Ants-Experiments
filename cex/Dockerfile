FROM python:3.11-slim
WORKDIR /app/cex
COPY main.py /app/cex/main.py
COPY requirements.txt /app/cex/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
