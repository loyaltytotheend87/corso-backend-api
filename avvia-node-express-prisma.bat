: Step 1 - Avvio di Docker Desktop
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

: Step 2 - Avvio dei contenitori e verifica degli stati

docker compose up -d
docker ps

: Step 3 - Avvio di node e del web server

cd "node-express-prisma"
npx nodemon --exec ts-node src/index.ts
