# SistemaJuanchOS

Una simulación educativa de un sistema operativo que implementa los conceptos fundamentales de los sistemas operativos modernos.

## Características

- Gestión de procesos (PCB - Process Control Block)
- Gestión de memoria (Memoria virtual y paginación)
- Sistema de archivos básico
- Interfaz de usuario en consola

## Estructura del Proyecto

```
SistemaJuanchOS/
├── src/
│   ├── kernel/
│   │   ├── process_manager.py
│   │   ├── memory_manager.py
│   │   └── file_system.py
│   ├── shell/
│   │   └── command_interface.py
│   └── main.py
├── tests/
│   └── test_kernel.py
└── README.md
```

## Requisitos

- Python 3.8 o superior

## Instalación

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`

## Uso

Ejecutar el sistema:
```bash
python src/main.py
```

## Comandos Disponibles

- `create_process`: Crear un nuevo proceso
- `list_processes`: Listar procesos activos
- `allocate_memory`: Asignar memoria
- `free_memory`: Liberar memoria
- `create_file`: Crear un archivo
- `list_files`: Listar archivos
- `exit`: Salir del sistema 