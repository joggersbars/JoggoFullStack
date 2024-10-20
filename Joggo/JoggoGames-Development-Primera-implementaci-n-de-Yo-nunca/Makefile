# Makefile

# Definición de Variables
IMAGE_NAME := joggo-games-template
ENV_PATH := C:/tmp/env.$(IMAGE_NAME)

# Verificar que .python-version existe
ifeq ($(wildcard .python-version),)
$(error Archivo .python-version no encontrado)
endif

# Leer la versión de Python desde .python-version
PYTHON_VERSION := $(shell type .python-version)
PYTHON_EXEC := py -$(PYTHON_VERSION)

# Objetivo por Defecto
all: create-environment

# Objetivo para Crear el Entorno Virtual
create-environment:
	@echo "Creando entorno virtual con Python $(PYTHON_VERSION)..."
	$(PYTHON_EXEC) -m venv $(ENV_PATH)
	@echo "Entorno virtual creado en $(ENV_PATH)."
	@echo "Instalando y actualizando pip..."
	$(ENV_PATH)/Scripts/python.exe -m pip install --upgrade pip
	@echo "Instalando dependencias desde requirements.txt..."
	$(ENV_PATH)/Scripts/python.exe -m pip install -r requirements.txt
	@echo "Entorno virtual creado y dependencias instaladas correctamente."

# Objetivo para Eliminar el Entorno Virtual (Opcional)
delete-environment:
	@echo "Eliminando entorno virtual en $(ENV_PATH)..."
	rmdir /S /Q $(ENV_PATH)
	@echo "Entorno virtual eliminado."

# Objetivo para Mostrar Ayuda (Opcional)
help:
	@echo "Objetivos Disponibles:"
	@echo "  create-environment   Crear y configurar el entorno virtual."
	@echo "  delete-environment   Eliminar el entorno virtual."
	@echo "  all                  Alias para create-environment."
	@echo "  help                 Mostrar esta ayuda."
