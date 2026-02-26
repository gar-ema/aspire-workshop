// ============================================================================
// Lab 3 — AppHost con Redis
// Sostituisci TUTTO il contenuto di weather-app/apphost.cs con questo file
// ============================================================================

// SDK Aspire 13.1 — niente .csproj necessario!
#:sdk Aspire.AppHost.Sdk@13.1.0

// Pacchetti NuGet importati direttamente come direttive
#:package Aspire.Hosting.Python@13.1.0
#:package Aspire.Hosting.JavaScript@13.1.0
// NUOVO: supporto Redis
#:package Aspire.Hosting.Redis@13.1.0

var builder = DistributedApplication.CreateBuilder(args);

// NUOVO: Redis — Aspire crea automaticamente un container Docker
var cache = builder.AddRedis("cache");

// Backend FastAPI — ora con riferimento a Redis
var app = builder.AddUvicornApp("app", "./app", "main:app")
    .WithUv()                           // usa "uv" come package manager (più veloce di pip)
    .WithExternalHttpEndpoints()        // espone l'endpoint all'esterno
    .WithReference(cache)               // NUOVO: inietta CACHE_URI come env var
    .WaitFor(cache)                     // NUOVO: aspetta che Redis sia pronto
    .WithHttpHealthCheck("/health");    // NUOVO: health check

// Frontend Vite+React
var frontend = builder.AddViteApp("frontend", "./frontend")
    .WithReference(app)                 // inietta APP_HTTP/APP_HTTPS nel frontend
    .WaitFor(app);                      // aspetta che il backend sia pronto

// NUOVO: in produzione, impacchetta il frontend nel backend come file statici
app.PublishWithContainerFiles(frontend, "./static");

builder.Build().Run();
