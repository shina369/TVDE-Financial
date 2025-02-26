#!/bin/bash
# Script de entrada para iniciar o MySQL com as permissões corretas
#!/bin/bash
# Ajustar as permissões de diretórios
chown -R mysql:mysql /var/lib/mysql
chmod -R 755 /var/lib/mysql

# Iniciar o MySQL
exec /usr/sbin/mysqld --user=mysql