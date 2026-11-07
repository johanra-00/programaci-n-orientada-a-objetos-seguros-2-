# EcoTech – Sistema de Gestión

## 1. Descripción del proyecto

EcoTech es un sistema desarrollado en Python para gestionar empleados, departamentos, proyectos y registros de tiempo. También incorpora autenticación de usuarios, control de permisos y consulta del indicador del dólar mediante una API externa.

## 2. Requisitos previos

Antes de comenzar, se deben instalar los siguientes programas:

- **Git:** para descargar el repositorio.
- **Python:** para ejecutar el sistema.
- **Visual Studio Code:** para abrir y trabajar con el código.

## 3. Descargar el proyecto desde GitHub

### Paso 1. Abrir Git Bash

Abrir Git Bash en la ubicación donde se desea guardar el proyecto.

### Paso 2. Clonar el repositorio

Ejecutar el siguiente comando:

```bash
git clone https://github.com/johanra-00/programaci-n-orientada-a-objetos-seguros-2-.git
```

Este comando descarga el proyecto desde GitHub.

### Paso 3. Ingresar a la carpeta

```bash
cd programaci-n-orientada-a-objetos-seguros-2-
```

### Paso 4. Abrir el proyecto en Visual Studio Code

```bash
code .
```

Este comando abre todos los archivos del proyecto en Visual Studio Code.

**Nota:** Para utilizar `code .`, Visual Studio Code debe estar instalado y configurado en el PATH del sistema.

## 4. Preparar el entorno de Python

### Paso 5. Crear un entorno virtual

Desde Git Bash, ejecutar:

```bash
py -m venv .venv
```

El entorno virtual permite instalar las dependencias del proyecto sin afectar otras instalaciones de Python.

### Paso 6. Activar el entorno virtual

```bash
source .venv/Scripts/activate
```

Si se activa correctamente, aparecerá `(.venv)` al comienzo de la línea de comandos.

### Paso 7. Instalar las dependencias

Ejecutar:

```bash
py -m pip install -r requirements.txt
```

Este comando instala las librerías necesarias para ejecutar EcoTech, como:

- bcrypt
- requests
- python-dotenv
- PyMySQL
- customtkinter

## 5. Configurar la base de datos

### Paso 8. Crear el archivo de configuración

En la carpeta principal del proyecto, crear un archivo llamado:

```text
.env
```

Dentro del archivo agregar:

```env
DB_ENGINE=sqlite
DB_NAME=ecotech.db
```

Esta configuración permite utilizar SQLite sin necesidad de instalar un servidor MySQL.

### Paso 9. Comprobar la base de datos

El proyecto incluye una base de datos llamada `ecotech.db` dentro de la carpeta `src`.

Comprobar que el archivo exista en:

```text
src/ecotech.db
```

**Importante:** No eliminar ni reemplazar este archivo, porque contiene información de prueba y cuentas registradas.

## 6. Ejecutar EcoTech

### Paso 10. Ingresar a la carpeta src

Desde Git Bash:

```bash
cd src
```

### Paso 11. Iniciar el programa

Ejecutar:

```bash
py main.py
```

Si todo está correctamente configurado, aparecerá la pantalla de inicio de sesión.

## 7. Utilización del sistema

Para ingresar al sistema se deben utilizar las credenciales correspondientes a una cuenta registrada.

### 7.1. Menú administrador

El administrador dispone de las siguientes opciones:

1. Registrar cuenta de empleado.
2. Listar empleados.
3. Consultar indicador del dólar.
4. Consultar historial de indicadores.
5. Consultar registros laborales generales.
9. Cerrar sesión.
0. Salir del programa.

### 7.2. Menú empleado

El empleado dispone de las siguientes opciones:

1. Consultar mi ficha.
2. Consultar mis registros de tiempo.
3. Modificar mis datos personales.
4. Consultar indicador del dólar.
5. Consultar historial de indicadores.
9. Cerrar sesión.
0. Salir del programa.

## 8. Consulta del indicador del dólar

El sistema consulta el valor del dólar mediante una API externa.

- Cuando la API responde correctamente, se obtiene el valor y se almacena en la base de datos.
- Si la API no está disponible, se intenta recuperar el último valor guardado.
- El historial permite consultar los valores almacenados anteriormente.

Para utilizar esta función se necesita conexión a Internet, aunque existe recuperación de información local cuando la API falla.

## 9. Cierre del programa

Para cerrar la sesión, seleccionar la opción `9`.

Para salir completamente del sistema, seleccionar la opción `0`.

Para desactivar el entorno virtual desde Git Bash:

```bash
deactivate
```

## 10. Consideraciones importantes

- No compartir las credenciales de acceso.
- No modificar directamente la base de datos.
- No eliminar el archivo `ecotech.db`.
- No compartir el archivo `.env`.
- Mantener instaladas las dependencias de `requirements.txt`.
- Se recomienda realizar copias de seguridad de la base de datos.
- Las credenciales de acceso deben ser proporcionadas por el administrador del sistema.

## 11. Tecnologías utilizadas

- Python.
- SQLite.
- MySQL (motor alternativo).
- Git y GitHub.
- Visual Studio Code.
- Requests.
- Bcrypt.
- Python-dotenv.
- API de tipo de cambio.