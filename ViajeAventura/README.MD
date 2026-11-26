# Viajes Aventura - Sistema de Gestión Turística

Sistema de consola desarrollado en Python bajo una **arquitectura de 4 capas** (`presentacion`, `negocio`, `persistencia`, `seguridad`) con soporte dual para **SQLite** y **MySQL**, sanitización estricta de entradas y hashing criptográfico nativo.

---

## Arquitectura del Proyecto

```text
ViajeAventura/
├── main.py                     # Punto de entrada principal del sistema
├── requirements.txt            # Dependencias opcionales (MySQL y dotenv)
├── .env                        # Configuración de motor de base de datos (opcional)
└── src/
    ├── presentacion/           # Interfaces de línea de comandos (CLIs por rol)
    ├── negocio/                # Modelos de dominio y servicios de lógica de negocio
    ├── persistencia/           # Conexión dual (SQLite/MySQL) y patrones DAO
    └── seguridad/              # Sanitización de entradas (InputSanitizer) y hashing PBKDF2
```

---

## Requisitos

* **Python 3.10 o superior.**
* **Visual Studio Code** y **Git Bash**.
* **Ejecución sin dependencias externas:** El sistema funciona de fábrica usando `sqlite3` y `hashlib` (`PBKDF2-HMAC-SHA256`), ambos incluidos en Python.
* **Dependencias opcionales** (solo si se conecta a MySQL o se usa `.env`):
  * `mysql-connector-python>=8.0.0`
  * `python-dotenv>=1.0.0`

---

## Ejecución Rápida en VS Code y Git Bash (Modo SQLite por defecto)

1. Abrir la carpeta `ViajeAventura` en **VS Code**.
2. Abrir la terminal integrada con **`Ctrl + ñ`** (o **`Ctrl + \``**) y seleccionar **Git Bash** en el selector de perfiles (o hacer clic derecho en la carpeta del proyecto y elegir **Open Git Bash here**).
3. Ejecutar el sistema:
   ```bash
   python main.py
   ```
   *(Si el comando `python` no responde, usar `py main.py`).*

Al iniciar, el sistema creará automáticamente la base de datos `src/ViajeAventura.DB`, las tablas y la cuenta de administrador por defecto.

---

## Instalación con Entorno Virtual y Soporte MySQL (Opcional)

Desde la terminal **Git Bash** (en VS Code o ventana externa) ubicada en la raíz del proyecto:

### 1. Crear y activar el entorno virtual

```bash
python -m venv .venv
source .venv/Scripts/activate
```
*(Verás el prefijo `(.venv)` en la terminal cuando esté activo).*

### 2. Instalar o actualizar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
```

### 3. Crear archivo de configuración `.env`

```bash
cat << 'EOF' > .env
# Opciones válidas: sqlite | mysql
DB_ENGINE=sqlite
SQLITE_PATH=src/ViajeAventura.DB

# Configuración requerida solo si DB_ENGINE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_DATABASE=viajes_aventura
EOF
```

### 4. Iniciar la aplicación

```bash
python main.py
```

*(Para volver a ejecutar el proyecto en el futuro, solo activa el entorno con `source .venv/Scripts/activate` y ejecuta `python main.py`).*

---

## Credenciales de Acceso Inicial

El sistema registra automáticamente un administrador al ejecutarse por primera vez:

    DEFAULT_ADMIN_EMAIL = "gerencia@viajesaventura.cl"
    DEFAULT_ADMIN_PASSWORD = "Aventura2026"
    
*(Los clientes pueden crear su propia cuenta desde la opción **2. Registrarse como cliente** en el menú principal).*

---

## Seguridad Implementada

* **Sanitización de entradas (`InputSanitizer`):** Validación estricta mediante expresiones regulares y bloqueo de secuencias peligrosas (`--`, `;`, `|`, `@`, `<`, `>`, comillas y caracteres de control) en nombres, destinos, países, documentos de identidad (RUT/Pasaporte), correos y montos.
* **Consultas parametrizadas:** Uso de marcadores `?` (SQLite) y `%s` (MySQL) en toda la capa DAO para prevenir inyección SQL.
* **Almacenamiento seguro de contraseñas:** Hashing mediante `PBKDF2-HMAC-SHA256` con 600.000 iteraciones, *salt* aleatorio de 128 bits y comparación en tiempo constante (`hmac.compare_digest`).