FROM python:3.11.11-alpine3.20

# Configuración de entorno
ENV PYTHONUNBUFFERED=1

# Configuración del directorio de trabajo
WORKDIR /app

# Actualizar los repositorios y agregar dependencias necesarias
RUN apk update \
    && apk add --no-cache \
       gcc \
       musl-dev \
       python3-dev \
       libffi-dev \
       jpeg-dev \
       zlib-dev \
       mariadb-dev \
       mariadb-connector-c-dev \
       build-base \
       linux-headers \
       pkgconfig \
    && pip install --upgrade pip

# Copiar y preparar las dependencias de Python
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copiar el código de la aplicación
COPY ./ ./

# Definir el comando de inicio
CMD ["sh", "entrypoint.sh"] 
# ejecutar script de bash en el entrypoint
