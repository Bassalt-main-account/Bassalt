@echo off
setlocal enabledelayedexpansion

:: Definir la carpeta donde están los archivos
set CONTAINER_DIR=Containers

:: Cargar variables desde el archivo .env dentro de Containers
if exist %CONTAINER_DIR%\.env (
    for /f "tokens=1,2 delims==" %%a in (%CONTAINER_DIR%\.env) do (
        set %%a=%%b
    )
) else (
    echo Error: No se encontro el archivo .env en %CONTAINER_DIR%. Asegurate de que existe.
    exit /b 1
)

:: Verifica si se paso un argumento
if "%1"=="" (
    echo ===============================
    echo  Docker PostgreSQL Manager
    echo ===============================
    echo Uso: docker_manager.bat [opcion]
    echo Opciones:
    echo   on          - Levanta y construye los contenedores
    echo   off         - Apagar los contenedores sin borrar datos
    echo   update      - Apaga y enciende contenedores (para actualizar API)
    echo   test        - Comprueba si la API está activa
    echo   db          - Conectarse a la base de datos PostgreSQL
    echo   activos     - Lista los contenedores activos
    echo   PURGE       - Regenera contenedores y estructura
    echo   renew       - PURGE + on
    echo ===============================
    exit /b 0
)

:: Mostrar ayuda si el argumento es --help
if "%1"=="--help" (
    echo ===============================
    echo  Docker PostgreSQL Manager
    echo ===============================
    echo Uso: docker_manager.bat [opcion]
    echo Opciones:
    echo   on          - Levanta y construye los contenedores
    echo   off         - Apagar los contenedores sin borrar datos
    echo   update      - Apaga y enciende contenedores (para actualizar API)
    echo   test        - Comprueba si la API está activa
    echo   db          - Conectarse a la base de datos PostgreSQL
    echo   activos     - Lista los contenedores activos
    echo   PURGE       - Regenera contenedores y estructura
    echo   renew       - PURGE + on
    echo ===============================
    exit /b 0
)

:: Ejecutar acciones segun el argumento proporcionado
if "%1"=="on" (
    echo Iniciando Docker Compose con build...
    docker-compose -f %CONTAINER_DIR%/docker-compose.yml up --build -d
    echo Contenedor iniciado.
    exit /b 0
)

if "%1"=="db" (
    echo Conectando a PostgreSQL...
    echo Ejecutando: docker exec -it %CONTAINER_NAME% psql -U %POSTGRES_USER% -d %POSTGRES_DB%
    docker exec -it %CONTAINER_NAME% psql -U %POSTGRES_USER% -d %POSTGRES_DB%
    echo NOTA: [ Si da error Postgres y el contenedor esta iniciado, dale unos segundos ]
    exit /b 0
)

if "%1"=="off" (
    echo Apagando los contenedores...
    docker-compose -f %CONTAINER_DIR%/docker-compose.yml down
    echo Contenedores detenidos.
    exit /b 0
)

if "%1"=="update" (
    echo Apagando los contenedores...
    docker-compose -f %CONTAINER_DIR%/docker-compose.yml down
    echo Contenedores detenidos.
    echo Iniciando Docker Compose con build...
    docker-compose -f %CONTAINER_DIR%/docker-compose.yml up --build -d
    echo Contenedor iniciado.
    exit /b 0
)

if "%1"=="updateAPI" (
    echo Reiniciando API...
    docker-compose -f %CONTAINER_DIR%/docker-compose.yml restart api
    echo Hecho.
    exit /b 0
)

if "%1"=="activos" (
    docker ps
    exit /b 0
)

if "%1"=="test" (
    echo Probando la API en http://127.0.0.1:8000/
    curl http://127.0.0.1:8000/
    echo.
    echo Probando la API en http://127.0.0.1:8001/
    curl http://127.0.0.1:8001/
    echo.
    exit /b 0
)

if "%1"=="PURGE" (
    echo Eliminando contenedores y datos...
    docker-compose -f %CONTAINER_DIR%/docker-compose.yml down -v
    rmdir /s /q %CONTAINER_DIR%\%VOLUME_NAME%
    rmdir /s /q %CONTAINER_DIR%\%VOLUME_DATA%
    echo Reinicio completado. Vuelve a ejecutar 'on' para iniciar PostgreSQL.
    exit /b 0
)

if "%1"=="renew" (
    echo Eliminando contenedores y datos...
    docker-compose -f %CONTAINER_DIR%/docker-compose.yml down -v
    rmdir /s /q %CONTAINER_DIR%\%VOLUME_NAME%
    rmdir /s /q %CONTAINER_DIR%\%VOLUME_DATA%
    echo Iniciando Docker Compose con build...
    docker-compose -f %CONTAINER_DIR%/docker-compose.yml up --build -d
    echo Contenedor iniciado.
    exit /b 0
)

:: Si el argumento no es valido
echo Error: Opcion no reconocida. Usa --help para ver las opciones.
exit /b 1