import os
import redis
from flask import Flask

app = Flask(__name__)

# --- КОНФИГУРАЦИЯ REDIS ---
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
# Используем try/except, чтобы приложение не падало, если порт придет кривой
try:
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
except ValueError:
    REDIS_PORT = 6379

# Подключаемся к Redis
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=2)

# --- ОСНОВНОЙ РОУТ ---
@app.route('/')
def hello():
    greeting = os.getenv('GREETING', 'Hello from Kubernetes!')
    pod_name = os.getenv('HOSTNAME', 'unknown')
    
    try:
        # Пытаемся увеличить счетчик
        hits = cache.incr('hits')
        db_status = f"Redis connected! Hits: {hits}"
    except redis.exceptions.ConnectionError:
        db_status = f"Redis NOT connected (Host: {REDIS_HOST}:{REDIS_PORT})"
    except Exception as e:
        db_status = f"Redis Error: {str(e)}"

    return f"""
    <h1>{greeting}</h1>
    <p>I am running on: <b>{pod_name}</b></p>
    <hr>
    <p>Database Status: <b>{db_status}</b></p>
    """

# --- РОУТЫ ДЛЯ KUBERNETES PROBES ---
@app.route('/health')
def health():
    """Liveness probe: Я жив?"""
    return "OK", 200

@app.route('/ready')
def ready():
    """Readiness probe: Я готов принимать трафик?"""
    # Можно добавить проверку, что Redis доступен, но пока просто вернем ОК
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

