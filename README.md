# Apptivity Setup Guide

Este archivo proporciona los pasos necesarios para configurar y ejecutar el proyecto **Apptivity** utilizando Docker,
así como una descripción de las herramientas que utiliza el proyecto.

## Descripción del Proyecto

Este repositorio contiene la API de APPTIVITY.
Además, esta pensado para levantar mediante docker la API y su base de datos PostgreSQL

## Dependencias

Este proyecto utiliza entre otras las siguientes herramientas y librerías:

- **[SQLAlchemy](https://www.sqlalchemy.org/)**: Un ORM para Python que facilita la interacción con bases de datos.
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)**: Herramienta de migración de bases de datos para SQLAlchemy.
- **[FastAPI](https://fastapi.tiangolo.com/)**: Un framework web moderno y rápido para construir APIs con Python 3.7+ basado en estándares como OpenAPI y JSON Schema.

## Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto.

### 1. Clonar el Repositorio

Clona el repositorio de GitHub en tu máquina local:

```bash
git clone https://github.com/pablovdt/apptivity.git
```

### 2. Muevete al repositorio recien clonado
```bash
cd apptivity
```

### 3. Construye el proyecto con Docker
```bash
sudo docker-compose --build
```

## Procedimientos SQL e inserciones de datos mediante archivo Python

### 4. Verfica el archivo necesario para procedimientos y triggers en Base de datos
```bash
ls -l ./database_procedures.sql
```

### 5. Copialo al contenedor
```bash
sudo docker cp ./database_procedures.sql db:/tmp/database_procedures.sql
```

### 6. Inicia los contenedores (api y bd)
```bash
sudo docker-compose up -d
```
### 7. Verifica que se ha copiado al contenedor
```bash
sudo docker exec -it db ls /tmp
```

### 8. Ejecuta las sentencias SQL
```bash
sudo docker exec -it db psql -U postgres -d apptivity -c "\i /tmp/database_procedures.sql"
```

### 9. Inserta datos en la bd (Municipios, categorias y niveles)
```bash
sudo docker exec -it apptivity /bin/bash
python3 insert_cities_and_categories_in_db.py
```
## Docker

### Si deseas detener los contenedores en ejecución, usa el siguiente comando:
```bash
sudo docker stop apptivity db
```
### Para volver a ejecutar los contenedores en segundo plano, usa el siguiente comando:
```bash
sudo docker-compose up -d
```
