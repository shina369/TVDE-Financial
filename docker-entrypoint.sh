#!/bin/bash
# Script de entrada para iniciar o MySQL com as permissões corretas

# Iniciar o servidor MySQL com a configuração padrão
exec /usr/sbin/mysqld --user=mysql
