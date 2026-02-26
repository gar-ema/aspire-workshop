# Lab 3: Introduci Nuove Modifiche al Template

## Prerequisito: aver completato Lab 2 (progetto ~/aspire-workshop/weather-app)

## Comandi

```bash
cd ~/aspire-workshop/weather-app
```

## File da modificare (in ordine)

1. **apphost.cs** — sostituisci tutto il contenuto con `apphost.cs` di questa cartella
2. **app/pyproject.toml** — sostituisci con `pyproject.toml` di questa cartella
3. **app/main.py** — sostituisci con `main.py` di questa cartella

```bash
# Avvia e verifica
aspire run
# → Dashboard: Resources (3 servizi: cache, app, frontend)
# → Structured Logs: filtra per "app" → "Cache MISS" poi "Cache HIT"
# → Traces: catena Frontend → API → Redis
# → Ctrl+C per fermare
```
