#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SistemaJuanchOS - Simulador de Sistema Operativo
===============================================

Este es el punto de entrada principal del sistema operativo simulado.
El sistema implementa las funcionalidades básicas de un sistema operativo:
- Gestión de usuarios y autenticación
- Sistema de archivos
- Gestión de procesos
- Gestión de memoria
- Interfaz gráfica de usuario

Autor: [Tu Nombre]
Versión: 1.0
"""

# Importación de módulos del sistema
import sys  # Para acceder a variables y funciones específicas del sistema
import os   # Para operaciones con el sistema de archivos

# Agregar el directorio src al path de Python para permitir importaciones relativas
current_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio actual
if current_dir not in sys.path:  # Verifica si el directorio ya está en el path
    sys.path.append(current_dir)  # Agrega el directorio al path si no está

# Importación de módulos de Qt para la interfaz gráfica
from PyQt5.QtWidgets import QApplication  # Clase principal para aplicaciones Qt

# Importación de los gestores del sistema
from kernel.user_manager import UserManager      # Gestor de usuarios
from kernel.file_system import FileSystem        # Sistema de archivos
from kernel.process_manager import ProcessManager # Gestor de procesos
from kernel.memory_manager import MemoryManager  # Gestor de memoria

# Importación de la interfaz gráfica
from gui.login_window import LoginWindow  # Ventana de inicio de sesión

def main():
    """
    Función principal que inicializa y ejecuta el sistema operativo.
    
    Esta función:
    1. Crea la aplicación Qt
    2. Inicializa los gestores del sistema
    3. Configura las dependencias entre gestores
    4. Muestra la ventana de login
    5. Ejecuta el bucle principal de la aplicación
    """
    try:
        # Crear la aplicación Qt
        app = QApplication(sys.argv)  # Inicializa la aplicación con los argumentos del sistema
        
        # Inicializar los gestores del sistema
        file_system = FileSystem()        # Crea el sistema de archivos
        process_manager = ProcessManager() # Crea el gestor de procesos
        memory_manager = MemoryManager()   # Crea el gestor de memoria
        user_manager = UserManager()       # Crea el gestor de usuarios
        
        # Configurar las dependencias entre gestores
        user_manager.set_managers(file_system, process_manager, memory_manager)  # Establece las dependencias
        
        # Crear y mostrar la ventana de login
        login_window = LoginWindow(user_manager)  # Crea la ventana de login
        login_window.show()  # Muestra la ventana
        
        # Ejecutar el bucle principal de la aplicación
        sys.exit(app.exec_())  # Inicia el bucle de eventos y maneja la salida
    except Exception as e:
        # Manejo de errores durante la inicialización
        print(f"Error al iniciar el sistema: {str(e)}")  # Muestra el error
        sys.exit(1)  # Termina la aplicación con código de error

# Punto de entrada del programa
if __name__ == '__main__':
    main()  # Ejecuta la función principal si el script se ejecuta directamente 