# Janus_PQC Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY janus_core.py janus_cli.py ./
CMD ["python", "janus_cli.py"]
