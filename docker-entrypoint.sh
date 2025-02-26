#!/bin/sh
set -e

# Executar migrações do banco, se necessário (exemplo)
# python manage.py migrate

# Iniciar a aplicação
exec "$@"
