@echo off
SET CONTAINER_DIR=Containers

:: Cargar variables de entorno desde el archivo .env
IF EXIST "%CONTAINER_DIR%\.env" (
    for /f "usebackq tokens=*" %%A in ("%CONTAINER_DIR%\.env") do set %%A
) ELSE (
    echo Error: No se encontró el archivo .env en %CONTAINER_DIR%. Asegúrate de que existe.
    exit /b 1
)
IF "%1"=="" (
    echo ===============================
    echo  Docker PostgreSQL Manager
    echo ===============================
    echo Uso: docker_manager.bat [opcion]
    echo Opciones:
    echo   on          - Levanta y construye los contenedores
    echo   off         - Apagar los contenedores sin borrar datos
    echo   update      - Apaga y enciende contenedores 
    echo   test        - Checkea si la API está up
    echo   db          - Conectarse a la base de datos PostgreSQL
    echo   activos     - Checkea qué contenedores están activos
    echo   PURGE       - Regenerar container y estructura
    echo   renew       - PURGE + on
    echo ===============================
    exit /b 0
)


IF "%1"=="--help" (
    echo ===============================
    echo  Docker PostgreSQL Manager
    echo ===============================
    echo Uso: docker_manager.bat [opcion]
    echo Opciones:
    echo   on          - Levanta y construye los contenedores
    echo   off         - Apagar los contenedores sin borrar datos
    echo   update      - Apaga y enciende contenedores 
    echo   test        - Checkea si la API está up
    echo   db          - Conectarse a la base de datos PostgreSQL
    echo   activos     - Checkea qué contenedores están activos
    echo   PURGE       - Regenerar container y estructura
    echo   renew       - PURGE + on
    echo ===============================
    exit /b 0
)

:: Ejecutar acciones según el argumento proporcionado
IF "%1"=="on" (
    echo Iniciando Docker Compose con build...
    docker-compose -f "%CONTAINER_DIR%\docker-compose.yml" up --build -d
    echo Contenedor iniciado.
    exit /b 0
)

IF "%1"=="db" (
    echo Conectando a PostgreSQL...
    docker exec -it "%CONTAINER_NAME%" psql -U "%POSTGRES_USER%" -d "%POSTGRES_DB%"
    echo NOTA: [ Si da error Postgres y el contenedor está iniciado, dale unos segundos ]
    exit /b 0
)

IF "%1"=="off" (
    echo Apagando los contenedores...
    docker-compose -f "%CONTAINER_DIR%\docker-compose.yml" down
    echo Contenedores detenidos.
    exit /b 0
)

IF "%1"=="update" (
    echo Apagando los contenedores...
    docker-compose -f "%CONTAINER_DIR%\docker-compose.yml" down
    echo Contenedores detenidos.
    echo Iniciando Docker Compose con build...
    docker-compose -f "%CONTAINER_DIR%\docker-compose.yml" up --build -d
    echo Contenedor iniciado.
    exit /b 0
)

IF "%1"=="updateAPI" (
    echo Reiniciando API...
    docker-compose -f "%CONTAINER_DIR%\docker-compose.yml" restart api
    echo Hecho.
    exit /b 0
)

IF "%1"=="activos" (
    docker ps
    exit /b 0
)

IF "%1"=="test" (
    curl "http://127.0.0.1:8000/"
    echo.
    curl "http://127.0.0.1:8001/"
    echo.
    exit /b 0
)

IF "%1"=="PURGE" (
    echo Eliminando contenedores y datos...
    docker-compose -f "%CONTAINER_DIR%\docker-compose.yml" down -v
    rmdir /s /q "%CONTAINER_DIR%\%VOLUME_NAME%"
    rmdir /s /q "%CONTAINER_DIR%\%VOLUME_DATA%"
    echo Reinicio completado. Vuelve a ejecutar "on" para iniciar PostgreSQL.
    exit /b 0
)

IF "%1"=="renew" (
    echo Eliminando contenedores y datos...
    docker-compose -f "%CONTAINER_DIR%\docker-compose.yml" down -v
    rmdir /s /q "%CONTAINER_DIR%\%VOLUME_NAME%"
    rmdir /s /q "%CONTAINER_DIR%\%VOLUME_DATA%"
    echo Iniciando Docker Compose con build...
    docker-compose -f "%CONTAINER_DIR%\docker-compose.yml" up --build -d
    echo Contenedor iniciado.
    exit /b 0
)
