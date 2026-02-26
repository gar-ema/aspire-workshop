# Lab 2: Crea e Avvia un'App da Template (15 min)

## Comandi da eseguire in sequenza

```bash
# 1. Crea il progetto dal template Python
cd ~/aspire-workshop
aspire new aspire-py-starter -n weather-app -o weather-app
cd weather-app

# 2. Esamina la struttura generata
cat apphost.cs
cat app/main.py
cat app/pyproject.toml
cat app/telemetry.py
cat frontend/package.json
cat frontend/vite.config.ts

# 3. Avvia l'applicazione
aspire run
# → Apri la Dashboard nel browser
# → Esplora: Resources, Endpoints, Structured Logs, Traces, Console
# → Ctrl+C per fermare
```

## Nessun file da creare — solo creazione da template e osservazione
