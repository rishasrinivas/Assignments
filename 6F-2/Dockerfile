FROM python:3.10-slim

WORKDIR /app

# copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy the project files (only what we need to serve)
COPY models /app/models
COPY src/serve /app/src/serve
WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "src.serve.app:app", "--host", "0.0.0.0", "--port", "8000"]
