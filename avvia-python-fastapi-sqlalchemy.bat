@echo off
echo Avvio di Docker Desktop...
start "" "C:\Users\michy\AppData\Local\Programs\DockerDesktop\Docker Desktop.exe"
echo Attendere l'avvio completo del motore Docker...
:attendiDocker
docker info >nul 2>&1
if errorlevel 1 (
    timeout /t 5 /nobreak >nul
    goto attendiDocker
)
echo Docker e' pronto!

:: Step 2 - Avvio dei contenitori e verifica degli stati
docker compose up -d
docker ps

:: Step 3 - Avvio di python e FastAPI
cd "python-fastapi-sqlalchemy"

echo Avvio del server FastAPI con Uvicorn...
:: Avvia Uvicorn in background o lancia il browser dopo un breve attimo
start http://localhost:8000/docs
venv\Scripts\uvicorn.exe main:app --reload --port 8000
