#!/bin/bash

# Definir la carpeta donde están los archivos
CONTAINER_DIR="Containers"

# Cargar variables de entorno desde el archivo .env dentro de Containers
if [ -f "$CONTAINER_DIR/.env" ]; then
    set -o allexport
    source "$CONTAINER_DIR/.env"
    set +o allexport
else
    echo "Error: No se encontró el archivo .env en $CONTAINER_DIR. Asegúrate de que existe."
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
    #echo "  updateAPI   - Apaga y enciende solo la API"
    echo "  test        - Checkea si la API esta up"
    echo "  db          - Conectarse a la base de datos PostgreSQL"
    echo "  activos     - Checkea qué contenedores están activos"
    echo "  PURGE       - Regenerar container y estructura"
    echo "  renew       - PURGE + on"
    echo "==============================="
    exit 0
}
#TODO: Opcion para reiniciar aislada base de datos e inserts


# Mostrar ayuda si el argumento es --help
display_help() {
    if [ -z "$1" ] || [ "$1" == "--help" ]; then
        help
    fi
}

display_help "$1"

# Ejecutar acciones según el argumento proporcionado
case "$1" in
    on)
        echo "Iniciando Docker Compose con build..."
        docker-compose -f "$CONTAINER_DIR/docker-compose.yml" up --build -d
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
        docker-compose -f "$CONTAINER_DIR/docker-compose.yml" down
        echo "Contenedores detenidos."
        ;;
    update)
        echo "Apagando los contenedores..."
        docker-compose -f "$CONTAINER_DIR/docker-compose.yml" down
        echo "Contenedores detenidos."
        echo "Iniciando Docker Compose con build..."
        docker-compose -f "$CONTAINER_DIR/docker-compose.yml" up --build -d
        echo "Contenedor iniciado."
        ;;
    updateAPI)
        echo "Reiniciando API"
        docker-compose -f "$CONTAINER_DIR/docker-compose.yml" restart api
        echo "Hecho."
        ;;
    activos)
        docker ps 
        ;;
    test)
        curl 'http://127.0.0.1:8000/'
        echo ''
        ;;
    PURGE)
        echo "Eliminando contenedores y datos..."
        docker-compose -f "$CONTAINER_DIR/docker-compose.yml" down -v
        rm -rf "$CONTAINER_DIR/$VOLUME_NAME"
        echo "Reinicio completado. Vuelve a ejecutar 'on' para iniciar PostgreSQL."
        ;;
    renew)
        echo "Eliminando contenedores y datos..."
        docker-compose -f "$CONTAINER_DIR/docker-compose.yml" down -v
        rm -rf "$CONTAINER_DIR/$VOLUME_NAME"
        echo "Iniciando Docker Compose con build..."
        docker-compose -f "$CONTAINER_DIR/docker-compose.yml" up --build -d
        echo "Contenedor iniciado."
        ;;
    *)
        help
        ;;
esac
