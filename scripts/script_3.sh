#!/bin/bash

# Autor: Felipe Valencia
# Version: 1
# Descripcion: Script que realiza la rotacion el control del disco
# basandose en dos umbrales determinados

# Inicio del script

# Configurar los valores de umbral
limit_disk_usage=80
emergency_disk_usage=90
# Numero maximo de intentos
max_attempts=5

# Lista de directorios para revisar los logs
trace_dirs=(
    "/var/log/apache2/"
    "/var/log/adminui/"
    "/var/log/postgresql/"
    "/opt/jans/jetty/jans-auth/logs/"
    "/opt/jans/jetty/jans-casa/logs/"
    "/opt/jans/jetty/jans-config-api/logs/"
    "/opt/jans/jetty/jans-fido2/logs/"
    "/opt/jans/jetty/jans-scim/logs/"
)

# Funcion para comprobar el uso de disco
function check_disk_usage() {
    disk_usage=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')
    echo "$disk_usage"
}

# Funcion para eliminar los logs antiguos
function delete_old_logs() {
    for dir in "${trace_dirs[@]}"; do
        echo "Eliminando logs en: $dir"
        find "$dir" -type f -name "*.gz" -exec rm -f {} \;
    done
}

# Funcion para ejecutar logrotate
function run_logrotate() {
    echo "Ejecutando logrotate..."
    /root/scripts/logrotate/logrotate.sh
}

# Comprobamos el estado del disco
disk_usage=$(check_disk_usage)
attempt=1

# Funcion principal para monitorizar y recuperar el espacio en disco
function main() {
    while [ "$disk_usage" -ge "$limit_disk_usage" ] && [ "$attempt" -le "$max_attempts" ]; do
        echo "Intento de recuperacion de disco #$attempt"

        if [ "$disk_usage" -ge "$emergency_disk_usage" ]; then
            echo "Espacio de disco mayor o igual a $emergency_disk_usage%. Ejecutando ciclo de emergencia..."
            run_logrotate
        fi

        echo "Eliminando logs antiguos..."
        delete_old_logs

        # Volver a comprobar el uso de disco
        disk_usage=$(check_disk_usage)

        # Si el espacio de disco es inferior al 80%, salimos del ciclo
        if [ "$disk_usage" -lt "$limit_disk_usage" ]; then
            echo "Espacio en disco inferior a $limit_disk_usage%. Recuperacion completa."
            break
        fi

        attempt=$((attempt+1))
    done

    # Si no se ha hecho ninguna accion y el espacio de disco es menor que los limites
    if [ "$disk_usage" -lt "$limit_disk_usage" ]; then
        echo "No se ha realizado ninguna accion. El espacio de disco es inferior a los limites establecidos."
    fi

    # Si alcanzamos el numero maximo de intentos
    if [ "$attempt" -gt "$max_attempts" ]; then
        echo "Se ha alcanzado el limite de intentos ($max_attempts). No se pudo liberar suficiente espacio en disco."
    fi
}

# Llamar a la funcion principal
main

# Fin del script
