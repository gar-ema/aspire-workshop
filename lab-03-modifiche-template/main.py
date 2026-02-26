# ============================================================================
# Lab 3 — Backend FastAPI con caching Redis
# Sostituisci TUTTO il contenuto di weather-app/app/main.py
# ============================================================================

import contextlib
import datetime
import json
import logging
import os
import random

import fastapi
import fastapi.responses
import fastapi.staticfiles
import opentelemetry.instrumentation.fastapi as otel_fastapi
import opentelemetry.instrumentation.redis as otel_redis
import redis
import telemetry


# Lifespan: configura OpenTelemetry all'avvio dell'app
@contextlib.asynccontextmanager
async def lifespan(app):
    telemetry.configure_opentelemetry()
    yield


app = fastapi.FastAPI(lifespan=lifespan)

# Instrumentazione automatica FastAPI — ogni richiesta genera una trace
otel_fastapi.FastAPIInstrumentor.instrument_app(app, exclude_spans=["send"])

# Client Redis globale — inizializzato lazy alla prima richiesta
redis_client = None

# Instrumentazione automatica Redis — ogni operazione Redis appare nelle trace
otel_redis.RedisInstrumentor().instrument()


def get_redis_client():
    """Ottieni l'istanza del client Redis.

    La connection string arriva dalla variabile d'ambiente CACHE_URI,
    iniettata automaticamente da Aspire tramite .WithReference(cache)
    """
    global redis_client
    if redis_client is None:
        # CACHE_URI è iniettata da Aspire (.WithReference(cache) nell'AppHost)
        if cache_uri := os.environ.get("CACHE_URI"):
            try:
                redis_client = redis.from_url(
                    cache_uri,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    decode_responses=True,
                )
            except Exception as e:
                logger.warning(f"Connessione Redis fallita: {e}")
                redis_client = None
        else:
            logger.info("CACHE_URI non trovata, caching disabilitato")
    return redis_client


logger = logging.getLogger(__name__)


# Pagina root — solo quando NON ci sono file statici del frontend
# (in produzione, PublishWithContainerFiles mette il frontend in ./static)
if not os.path.exists("static"):
    @app.get("/", response_class=fastapi.responses.HTMLResponse)
    async def root():
        return "API attiva. Vai a <a href='/api/weatherforecast'>/api/weatherforecast</a>"


@app.get("/api/weatherforecast")
async def weather_forecast(redis_client=fastapi.Depends(get_redis_client)):
    """Endpoint previsioni meteo con caching Redis.

    - Prima richiesta: Cache MISS → genera dati → salva in Redis (TTL 5s)
    - Richieste successive (entro 5s): Cache HIT → dati da Redis

    Osserva nella Dashboard:
    - Structured Logs: messaggi "Cache HIT" vs "Cache MISS"
    - Traces: operazioni GET/SET verso Redis
    """
    cache_key = "weatherforecast"

    # Prova a leggere dalla cache
    if redis_client:
        try:
            cached = redis_client.get(cache_key)
            if cached:
                logger.info("Cache HIT — dati dalla cache Redis")
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Errore lettura cache: {e}")

    # Cache MISS — genera dati freschi
    logger.info("Cache MISS — generazione dati freschi")
    summaries = ["Gelido", "Freddo", "Fresco", "Mite", "Caldo", "Torrido", "Rovente"]
    forecast = []
    for i in range(1, 6):
        temp_c = random.randint(-20, 55)
        forecast.append({
            "date": (datetime.datetime.now() + datetime.timedelta(days=i)).isoformat(),
            "temperatureC": temp_c,
            "temperatureF": int(temp_c * 9 / 5) + 32,
            "summary": random.choice(summaries),
        })

    # Salva in cache con TTL di 5 secondi
    if redis_client:
        try:
            redis_client.setex(cache_key, 5, json.dumps(forecast))
        except Exception as e:
            logger.warning(f"Errore scrittura cache: {e}")

    return forecast


@app.get("/health", response_class=fastapi.responses.PlainTextResponse)
async def health_check(redis_client=fastapi.Depends(get_redis_client)):
    """Health check — usato da Aspire (.WithHttpHealthCheck("/health"))
    per verificare che il servizio sia attivo e Redis raggiungibile."""
    if redis_client:
        redis_client.ping()
    return "Healthy"


# Serve i file statici del frontend dalla root
# (attivo solo quando ./static esiste, cioè dopo PublishWithContainerFiles)
if os.path.exists("static"):
    app.mount("/", fastapi.staticfiles.StaticFiles(directory="static", html=True), name="static")
