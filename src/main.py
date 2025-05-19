#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo Principal del Sistema Operativo
====================================

Este módulo implementa el punto de entrada principal del sistema operativo,
incluyendo:
- Inicialización del sistema
- Gestión de usuarios
- Sistema de archivos
- Gestión de procesos
- Gestión de memoria
- Interfaz gráfica

Funciones:
----------
- main(): Función principal de inicialización
"""

# Importación de módulos del sistema
import sys  # Para variables y funciones específicas del sistema
import os   # Para operaciones del sistema de archivos

# Agregar el directorio src al path de Python para permitir importaciones relativas
current_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio actual
if current_dir not in sys.path:  # Verifica si el directorio ya está en el path
    sys.path.append(current_dir)  # Agrega el directorio al path si no está

# Importación de módulos de Qt para la interfaz gráfica
from PyQt5.QtWidgets import QApplication  # Clase principal para aplicaciones Qt
from PyQt5.QtCore import Qt

# Importación de los gestores del sistema
from core.user_manager import UserManager      # Gestor de usuarios
from core.file_system import FileSystem        # Sistema de archivos
from core.process_manager import ProcessManager # Gestor de procesos
from core.memory_manager import MemoryManager  # Gestor de memoria

# Importación de la interfaz gráfica
from gui.login_window import LoginWindow  # Ventana de inicio de sesión

def main():
    """
    Función principal que inicializa y ejecuta el sistema operativo.
    
    Esta función:
    1. Crea la aplicación Qt
    2. Inicializa los gestores del sistema
    3. Configura las dependencias entre gestores
    4. Muestra la ventana de inicio de sesión
    5. Ejecuta el bucle principal de la aplicación
    
    Returns:
        int: Código de salida de la aplicación
    """
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno y consistente
    
    try:
        # Inicializar los gestores del sistema
        file_system = FileSystem()        # Crea el sistema de archivos
        process_manager = ProcessManager() # Crea el gestor de procesos
        memory_manager = MemoryManager()   # Crea el gestor de memoria
        user_manager = UserManager()       # Crea el gestor de usuarios
        
        # Configurar dependencias entre gestores
        user_manager.file_system = file_system
        process_manager.memory_manager = memory_manager
        
        # Mostrar la ventana de inicio de sesión
        login_window = LoginWindow(user_manager, file_system, process_manager, memory_manager)  # Crea la ventana de login
        login_window.show()  # Muestra la ventana
        
        # Ejecutar el bucle principal
        return app.exec_()
        
    except Exception as e:
        # Manejo de errores durante la inicialización
        print(f"Error al iniciar el sistema: {e}")  # Muestra el error
        return 1  # Termina la aplicación con código de error

# Punto de entrada del programa
if __name__ == "__main__":
    sys.exit(main())  # Ejecuta la función principal si el script se ejecuta directamente 