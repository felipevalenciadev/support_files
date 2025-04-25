# Configuracion para logs de adminui
/var/log/adminui/*.log /var/log/adminui/*.log-* /var/log/adminui/*.log.* {
    daily
    rotate 15
    compress
    missingok
    notifempty
    dateext
    create
    sharedscripts
}

# Configuracion para logs de jans-auth
/opt/jans/jetty/jans-auth/logs/*.log /opt/jans/jetty/jans-auth/logs/*.log-* /opt/jans/jetty/jans-auth/logs/*.log.* {
    daily
    rotate 15
    compress
    missingok
    notifempty
    dateext
    create
    sharedscripts
}

# Configuracion para logs de jans-casa
/opt/jans/jetty/jans-casa/logs/*.log /opt/jans/jetty/jans-casa/logs/*.log-* /opt/jans/jetty/jans-casa/logs/*.log.* {
    daily
    rotate 15
    compress
    missingok
    notifempty
    dateext
    create
    sharedscripts
}

# Configuracion para logs de jans-config-api
/opt/jans/jetty/jans-config-api/logs/*.log /opt/jans/jetty/jans-config-api/logs/*.log-* /opt/jans/jetty/jans-config-api/logs/*.log.* {
    daily
    rotate 15
    compress
    missingok
    notifempty
    dateext
    create
    sharedscripts
}

# Configuracion para logs de jans-fido2
/opt/jans/jetty/jans-fido2/logs/*.log /opt/jans/jetty/jans-fido2/logs/*.log-* /opt/jans/jetty/jans-fido2/logs/*.log.* {
    daily
    rotate 15
    compress
    missingok
    notifempty
    dateext
    create
    sharedscripts
}

# Configuracion para logs de jans-scim
/opt/jans/jetty/jans-scim/logs/*.log /opt/jans/jetty/jans-scim/logs/*.log-* /opt/jans/jetty/jans-scim/logs/*.log.* {
    daily
    rotate 15
    compress
    missingok
    notifempty
    dateext
    create
    sharedscripts
}
