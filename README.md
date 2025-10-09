# Proyecto Integrador: Memorama Cognitivo

## 1. Introducción

Este documento establece las directrices, estándares y flujo de trabajo para el desarrollo del Proyecto Integrador. Su objetivo es unificar nuestras prácticas de colaboración y asegurar la calidad del producto final. Se espera que todos los miembros del equipo conozcan y apliquen los principios aquí descritos.

## 2. Descripción del Proyecto

### 2.1. Objetivo General

Desarrollar una aplicación de escritorio en `Python` que, mediante un juego de memorama, contribuya a la estimulación y el mantenimiento de las capacidades cognitivas de los usuarios.

### 2.2. Características Funcionales

- **Tablero de Juego**: La interfaz principal consistirá en un tablero (matriz) de 5x5.
- **Generación de Fichas**: El programa generará pares de fichas (símbolos, colores o números) y los distribuirá de forma aleatoria en el tablero al inicio de cada partida.
- **Mecánica Principal**: El usuario seleccionará dos casillas del tablero.
    - Si las fichas son idénticas (un par), permanecerán visibles.
    - Si son diferentes, se ocultarán después de un breve periodo.
- **Condiciones de Victoria**: El juego concluye cuando el usuario ha encontrado todos los pares de fichas en el tablero. Se registrará el número total de intentos.

### 2.3. Stack Tecnológico

- **Lenguaje**: `Python 3.x`
- **Interfaz Gráfica (GUI)**: `Tkinter`

## 3. Roles y Responsabilidades

Para una gestión eficiente del proyecto, se han definido los siguientes roles. Si bien la colaboración en el desarrollo es transversal, cada rol tiene un enfoque principal:

- **Líder de Proyecto (Scrum Master)**:
    - **Actividades**: Gestionar el backlog del producto, planificar las tareas, facilitar las reuniones del equipo, eliminar impedimentos y asegurar el cumplimiento de los objetivos de cada entrega.

- **Desarrollador(es)**:
    - **Actividades**: Implementar las funcionalidades del juego, escribir código limpio y modular, participar en las revisiones de código y documentar las funciones desarrolladas.

- **Líder de QA (Calidad)**:
    - **Actividades**: Diseñar el plan de pruebas, ejecutar casos de prueba para cada función, reportar incidencias (bugs), y validar que el software cumpla con los requisitos especificados.

- **Líder de Soporte (Control de Versiones)**:
    - **Actividades**: Administrar el repositorio en GitHub, supervisar el flujo de trabajo de ramas (branching), gestionar la fusión de código (merges) y asegurar la integridad del control de versiones.

## 4. Estándares de Codificación

La consistencia en el código es fundamental para la legibilidad y el mantenimiento. El equipo se adhiere a los siguientes estándares:

### 4.1. Convenciones de Nomenclatura

- **Variables y Funciones**: `camelCase`. Deben ser descriptivos y autoexplicativos.
    - Ejemplo: `tarjetaSeleccionada`, `verificarPares()`.
- **Constantes**: `SNAKE_CASE_MAYUSCULAS`.
    - Ejemplo: `TAMANO_TABLERO = 5`, `TIEMPO_VISTA_PREVIA = 1`.

### 4.2. Documentación de Funciones

Toda función deberá incluir un docstring que explique su propósito, argumentos y valor de retorno, siguiendo el formato de Google.

```python
def inicializarTablero(tamano):
    """Crea y llena el tablero con los pares de fichas.

    Args:
        tamano (int): El número de filas y columnas del tablero (debe ser impar).

    Returns:
        list: Una matriz (lista de listas) que representa el tablero de juego.
    """
    # Código de la función
    pass
```

## 5. Flujo de Trabajo con Git y GitHub

Se implementará un flujo de trabajo basado en Git Flow para garantizar un control de versiones ordenado y prevenir conflictos.

### 5.1. Ramas (Branches)

- `main`: Rama principal. Contiene únicamente el código de producción estable. No se realizan commits directos a esta rama.
- `develop`: Rama de integración. Es la base para el desarrollo de nuevas funcionalidades.
- `feature/nombre-funcionalidad`: Cada nueva tarea o funcionalidad se desarrollará en una rama propia creada a partir de `develop`.
    - Ejemplo: `feature/interfaz-grafica`, `feature/logica-turnos`.

### 5.2. Mensajes de Commit

Los mensajes de commit deben ser claros y seguir el estándar de "Conventional Commits" para facilitar la trazabilidad.

- **Formato**: `tipo(alcance): descripción breve`
- **Tipos comunes**: `feat` (nueva funcionalidad), `fix` (corrección de error), `docs` (documentación), `style` (formato), `refactor` (reestructuración de código), `test` (pruebas).
- **Ejemplo**: `feat(tablero): implementa la función para barajar las fichas`

### 5.3. Pull Requests (PRs)

Al completar una funcionalidad en una rama `feature`, se abrirá un Pull Request hacia la rama `develop`.

Todo PR deberá ser revisado y aprobado por al menos un miembro del equipo (distinto al autor) antes de ser fusionado.

## 6. Estructura del Proyecto

La organización de los archivos y directorios del proyecto será la siguiente:

```
proyecto-memorama/
│
├── memorama/
│   ├── __init__.py      # Necesario para que Python trate la carpeta como un paquete
│   ├── tablero.py       # Lógica para crear y manipular el estado del tablero
│   ├── interfaz.py      # Código relacionado con la GUI (Tkinter)
│   └── main.py          # Punto de entrada para ejecutar la aplicación
│
├── tests/
│   ├── test_tablero.py  # Pruebas unitarias para la lógica del tablero
│   └── ...
│
├── .gitignore           # Archivo para ignorar directorios (ej. __pycache__)
│
└── README.md            # Este documento
```