#!/bin/bash

# echo "Esperando a que la base de datos esté lista..."
# while ! nc -z db 5432; do
  # sleep 0.1
# done
# echo "Base de datos lista"
#!/bin/bash

echo "Esperando a que la base de datos esté lista..."
while ! nc -z postgres.railway.internal 5432; do
  sleep 0.1
done
echo "Base de datos lista"

