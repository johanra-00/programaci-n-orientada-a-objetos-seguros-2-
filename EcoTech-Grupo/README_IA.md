
## Historial de problemas y uso de Inteligencia Artificial

### 1. Problemas encontrados y soluciones aplicadas

Durante el desarrollo de EcoTech se presentaron diferentes errores de programación y persistencia de datos. Para resolverlos se revisó el código, se analizaron los mensajes de error y se realizaron modificaciones para adaptar las soluciones a la estructura del proyecto.

**Problema 1: Importación circular entre clases**

Se produjo un error de importación entre las clases `Empleado` y `Departamento`. Para solucionarlo, se revisaron las dependencias y los imports entre los módulos, con el objetivo de evitar que las clases se intentaran importar mutuamente de forma incorrecta.

**Problema 2: Módulos no encontrados**

Python indicó que no encontraba módulos como `registro_tiempo` y `generar_informe`. Se revisaron los nombres de los archivos, sus ubicaciones y las instrucciones de importación para que coincidieran con la estructura del proyecto.

**Problema 3: Método ubicado fuera de su clase**

El método `asignar_seguridad` estaba fuera de la clase `SistemaAutentificacion`. Se corrigió la indentación para que el método perteneciera a la clase correspondiente, respetando la estructura de Python.

**Problema 4: Atributos y métodos faltantes**

Aparecieron errores relacionados con atributos y métodos como `telefono`, `agregar_informes` y `agregar_informe`. Se revisaron las definiciones y las llamadas para que los nombres coincidieran y los métodos estuvieran disponibles donde se necesitaban.

**Problema 5: Error al guardar un departamento**

Se produjo un error porque el nombre de un departamento se interpretaba como una tupla en lugar de una cadena de texto. Se corrigió la asignación del atributo `nombre`, eliminando la coma que generaba ese tipo de dato.

**Problema 6: Problemas de conexión con MySQL**

La conexión con MySQL presentó un error de conexión rechazada (`WinError 10061`). Se revisó la configuración y se continuó el desarrollo utilizando SQLite, lo que permitió seguir trabajando en la persistencia sin depender de un servidor MySQL.

**Problema 7: Operaciones incompletas en el DAO de departamentos**

Inicialmente, el DAO de departamentos tenía implementada principalmente la inserción. Se agregaron operaciones para listar, buscar, actualizar y eliminar departamentos mediante consultas SQL, permitiendo gestionar los registros desde el programa.

**Problema 8: Persistencia de proyectos**

Era necesario almacenar y recuperar proyectos desde la base de datos. Se trabajó en la clase `ProyectoDAO` y en la creación de la tabla `proyecto`. Durante las pruebas se logró insertar un proyecto y comprobar que aparecía en el listado.

**Problema 9: Errores de indentación en el menú principal**

Se encontraron problemas en la organización de los bloques condicionales del menú principal. Se corrigió la indentación y se organizaron las llamadas a los submenús para facilitar la navegación por las opciones del sistema.

### 2. Evaluación de las sugerencias de IA

La inteligencia artificial se utilizó como apoyo para analizar errores, comprender mensajes de Python, proponer modificaciones y organizar algunas operaciones del programa.

**Sugerencias adoptadas:** se utilizaron propuestas para corregir imports, organizar los menús y desarrollar operaciones CRUD en los DAO.

**Sugerencias modificadas:** se adaptaron las soluciones a los nombres reales de los archivos, las clases, los atributos y la configuración de la base de datos de EcoTech.

**Sugerencias que requieren revisión:** los métodos de algunas clases y las relaciones entre las entidades deben revisarse para asegurar que coincidan con el diagrama UML y los requisitos del proyecto.

Las sugerencias no se consideran correctas automáticamente; deben revisarse y probarse antes de incorporarlas definitivamente.

### 3. Pruebas realizadas

Durante el desarrollo se realizaron pruebas de inserción y listado.

En departamentos, se insertó un registro y se obtuvo un identificador. También se comprobó que el departamento aparecía en el listado.

En proyectos, se insertó un proyecto y se comprobó que aparecía en el listado con su identificador, nombre y descripción.

Las operaciones de búsqueda, actualización y eliminación, así como el funcionamiento completo de los menús, deben verificarse con pruebas adicionales antes de considerarse completamente comprobadas.

### 4. Mejoras pendientes

Se debe continuar revisando la correspondencia entre el diagrama UML, las clases de Python y las tablas de la base de datos. También es necesario comprobar las relaciones entre las entidades, completar las validaciones de datos y verificar las operaciones CRUD de todas las entidades requeridas.

Además, se deben revisar los métodos que todavía contienen implementaciones incompletas y comprobar que su comportamiento corresponda con los requisitos establecidos.

### 5. Transparencia y responsabilidad en el uso de IA

La inteligencia artificial se utilizó como herramienta de apoyo durante el desarrollo de EcoTech. Sus sugerencias fueron revisadas y adaptadas según los problemas encontrados en el código.

El equipo es responsable de comprender las modificaciones realizadas, justificar técnicamente las decisiones y demostrar el funcionamiento del programa mediante pruebas. La IA facilita el proceso de desarrollo, pero no reemplaza la revisión ni la comprensión del código. 
La semilla no se ejecutaba: el archivo no tenía la función principal cargar_semilla() ni la llamada para iniciar el proceso. Se agregaron para ejecutar la carga de datos.

Datos duplicados: se incorporaron consultas para comprobar si los departamentos y empleados ya existían antes de insertarlos.

Cantidad incorrecta de registros: la base de datos tenía departamentos y un empleado de prueba que superaban las cantidades solicitadas. Se eliminaron esos registros sobrantes para dejar 5 departamentos y 20 empleados.

Confirmación de los cambios: se agregó commit() para guardar los registros y rollback() para revertir los cambios si ocurre un error.

Cierre de conexión: se agregó finally con close() para cerrar la conexión con la base de datos al terminar el proceso.