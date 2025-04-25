#!/bin/bash

# Autor: Felipe Valencia
# Version: 1
# Descripcion: Script que realiza la rotacion de logs, comprueba directorios
# especifico eliminando archivos resultantes con "0 bytes" y reinicia
# todos los servicios para la creacion de nuevos archivos de log

# Inicio del script

# Directorios de comprobacion de logs
trace_dirs=(
    "/var/log/adminui/"
    "/opt/jans/jetty/jans-auth/logs/"
    "/opt/jans/jetty/jans-casa/logs/"
    "/opt/jans/jetty/jans-config-api/logs/"
    "/opt/jans/jetty/jans-fido2/logs/"
    "/opt/jans/jetty/jans-scim/logs/"
)

# 1. Forzar la rotacion de logs
echo "Forzando la rotacion de logs..."
sudo logrotate -f /etc/logrotate.conf

# 2. Eliminar archivos de logs vacios en los directorios determinados
echo "Eliminando archivos vacios de logs temporales..."
for dir in "${trace_dirs[@]}"; do
    if [ -d "$dir" ]; then
        # Buscar y eliminar archivos con 0 bytes
        find "$dir" -type f \( -name "*.log" -or -name "*.log-*" -or -name "*.log.*" \) -size 0 -exec rm -f {} \;
    else
        echo "Directorio no encontrado: $dir"
    fi
done

# 3. Ejecutar reinicio del servicio Jans
echo "Reiniciando el servicio jans..."
jans restart
echo "Proceso completado."

# Fin del script
