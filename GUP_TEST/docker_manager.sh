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

help() { 
    echo "==============================="
    echo " Docker PostgreSQL Manager"
    echo "==============================="
    echo "Uso: ./docker_manager.sh [opcion]"
    echo "Opciones:"
    echo "  on          - Levanta y construye los contenedores"
    echo "  off         - Apagar los contenedores sin borrar datos"
    echo "  update      - Apaga y enciende contenedores (para actualizar api)"
    echo "  updateAPI   - Apaga y enciende solo la API"
    echo "  db          - Conectarse a la base de datos PostgreSQL"
    echo "  activos     - Checkea que contenedores estan activos"
    echo "  PURGE       - Regenerar container y estructura"
    echo "==============================="
    exit 0
    # meter algo para docker-compose restart api
}

# Mostrar ayuda si el argumento es --help
if [ -z "$1" ] || [ "$1" == "--help" ] ; then
    help
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
    update)
        echo "Apagando los contenedores..."
        docker-compose down
        echo "Contenedores detenidos."
        echo "Iniciando Docker Compose con build..."
        docker-compose up --build -d
        echo "Contenedor iniciado."
        ;;
    updateAPI)
        echo "Reiniciando API"
        docker-compose restart api
        echo "Hecho."
        ;;
    activos)
        docker ps 
        ;;
    PURGE)
        echo "Eliminando contenedores y datos..."
        docker-compose down -v
        rm -rf "$VOLUME_NAME"
        echo "Reinicio completado. Vuelve a ejecutar 'on' para iniciar PostgreSQL."
        ;;
    *)
        help
        ;;
esac
