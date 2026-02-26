# Lab 1: Esplora i Template

## Comandi da eseguire in sequenza

```bash
# 1. Crea la cartella di lavoro
mkdir ~/aspire-workshop && cd ~/aspire-workshop

# 2. Mostra i template disponibili (Ctrl+C per uscire)
aspire new

# 3. Crea il template C# (project-based AppHost)
aspire new aspire-starter -n app-csharp -o app-csharp

# 4. Crea il template Python (single-file AppHost)
aspire new aspire-py-starter -n app-python -o app-python

# 5. Confronta le strutture
find app-csharp -type f | head -20
cat app-csharp/app-csharp.AppHost/AppHost.cs
cat app-csharp/app-csharp.AppHost/app-csharp.AppHost.csproj

find app-python -type f | head -20
cat app-python/apphost.cs

# 6. Crea un AppHost vuoto (minimo assoluto)
aspire new aspire-apphost-singlefile -n empty-host -o empty-host
cat empty-host/apphost.cs
```

## Nessun file da creare — solo esplorazione dei template generati
