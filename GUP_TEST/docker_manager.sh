#!/bin/bash

# Cargar variables de entorno desde el archivo .env de forma segura
if [ -f .env ]; then
    set -o allexport
    source .env
    set +o allexport
else
    echo "Error: No se encontró el archivo .env. Asegúrate de que existe en el mismo directorio que este script."
    exit 1
fi

# Verifica si se pasó un argumento
if [ -z "$1" ]; then
    echo "Error: Debes proporcionar un argumento. Usa --help para ver las opciones."
    exit 1
fi

# Mostrar ayuda si el argumento es --help
if [ "$1" == "--help" ]; then
    echo "==============================="
    echo " Docker PostgreSQL Manager"
    echo "==============================="
    echo "Uso: ./docker_manager.sh [opcion]"
    echo "Opciones:"
    echo "  on      - Levanta y construye los contenedores"
    echo "  db      - Conectarse a la base de datos PostgreSQL"
    echo "  off     - Apagar los contenedores sin borrar datos"
    echo "  restart - Regenerar container y estructura"
    echo "==============================="
    exit 0
fi

# Ejecutar acciones según el argumento proporcionado
case "$1" in
    on)
        echo "Iniciando Docker Compose con build..."
        docker-compose up --build -d
        echo "Contenedor iniciado."
        ;;
    db)
        echo "Conectando a PostgreSQL..."
        echo "Ejecutando: docker exec -it \"$CONTAINER_NAME\" psql -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\""
        docker exec -it "$CONTAINER_NAME" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" 
        echo "NOTA: [ Si da error Postgres y el contenedor está iniciado, dale unos segundos ]"
        ;;
    off)
        echo "Apagando los contenedores..."
        docker-compose down
        echo "Contenedores detenidos."
        ;;
    restart)
        echo "Eliminando contenedores y datos..."
        docker-compose down -v
        rm -rf "$VOLUME_NAME"
        echo "Reinicio completado. Vuelve a ejecutar 'on' para iniciar PostgreSQL."
        ;;
    *)
        echo "Error: Opción no reconocida. Usa --help para ver las opciones."
        exit 1
        ;;
esac
