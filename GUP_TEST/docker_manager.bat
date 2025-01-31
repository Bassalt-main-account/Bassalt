@echo off
setlocal

:: Verifica si se pasó un argumento
if "%1"=="" (
    echo Error: Debes proporcionar un argumento. Usa --help para ver las opciones.
    exit /b 1
)

:: Mostrar ayuda si el argumento es --help
if "%1"=="--help" (
    echo ===============================
    echo  Docker PostgreSQL Manager
    echo ===============================
    echo Uso: docker_manager.bat [opcion]
    echo Opciones:
    echo   on      - Levanta y construye los contenedores
    echo   db      - Conectarse a la base de datos PostgreSQL
    echo   off     - Apagar los contenedores sin borrar datos
    echo   restart - Regenerar container y estructura
    echo ===============================
    exit /b 0
)

:: Ejecutar acciones según el argumento proporcionado
if "%1"=="on" (
    echo Iniciando Docker Compose con build...
    docker-compose up --build -d
    echo Contenedor iniciado.
    exit /b 0
)

if "%1"=="db" (
    echo Conectando a PostgreSQL...
    docker exec -it postgres_container psql -U user -d mydatabase
    echo 
    echo NOTA: [ Si da error Postgres y el contenedor esta iniciado dadle unos segundos ]
    exit /b 0
)

if "%1"=="off" (
    echo Apagando los contenedores...
    docker-compose down
    echo Contenedores detenidos.
    exit /b 0
)

if "%1"=="restart" (
    echo Eliminando contenedores y datos...
    docker-compose down -v
    rmdir /s /q postgres_data
    echo Reinicio completado. Vuelve a ejecutar 'on' para iniciar PostgreSQL.
    exit /b 0
)

:: Si el argumento no es válido
echo Error: Opción no reconocida. Usa --help para ver las opciones.
exit /b 1
