FROM python:3.11-slim
RUN apt-get update && apt-get install -y tini && apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "app.py"]
