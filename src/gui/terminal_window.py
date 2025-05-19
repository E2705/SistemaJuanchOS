#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Terminal del Sistema Operativo
======================================

Este módulo implementa la interfaz gráfica de la terminal del sistema operativo,
incluyendo:
- Terminal interactiva
- Historial de comandos
- Autocompletado
- Colores personalizados
- Integración con el sistema de archivos y procesos

Clases:
--------
- TerminalWindow: Ventana principal de la terminal
"""

# Importación de módulos de Qt para la interfaz gráfica
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTextEdit,
                           QLineEdit, QPushButton, QHBoxLayout, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QTextCursor, QColor, QTextCharFormat

# Importación de módulos del sistema
import sys
import os

# Importación de módulos locales
from core.file_system import FileSystem
from core.process_manager import ProcessManager
from core.memory_manager import MemoryManager
from core.command_interface import CommandInterface

class TerminalWindow(QMainWindow):
    """
    Implementa la ventana principal de la terminal del sistema operativo.
    
    Atributos:
        user_manager: Gestor de usuarios del sistema
        file_system: Sistema de archivos
        process_manager: Gestor de procesos
        memory_manager: Gestor de memoria
        command_interface: Interfaz de comandos
        output_text: Widget de texto para la salida
        input_line: Widget de línea para la entrada
        command_history: Lista de comandos ejecutados
        current_history_index: Índice actual en el historial
        prompt: Símbolo del prompt
        current_dir: Directorio actual
    """
    
    def __init__(self, user_manager, parent=None):
        """
        Inicializa la ventana de la terminal.
        
        Args:
            user_manager: Gestor de usuarios del sistema
            parent: Widget padre
        """
        super().__init__(parent)
        self.user_manager = user_manager
        
        # Inicializa los gestores del sistema
        self.file_system = FileSystem()
        self.process_manager = ProcessManager()
        self.memory_manager = MemoryManager()
        
        # Configura la interfaz de comandos
        self.command_interface = CommandInterface(
            self.file_system,
            self.process_manager,
            self.memory_manager,
            self.user_manager
        )
        
        # Inicializa variables de estado
        self.command_history = []
        self.current_history_index = -1
        self.prompt = "$ "
        self.current_dir = "/"
        
        # Configura la interfaz
        self.init_ui()
        self.show_welcome_message()

    def init_ui(self):
        """
        Inicializa la interfaz de usuario de la terminal.
        Configura la ventana, el área de texto y la línea de entrada.
        """
        self.setWindowTitle('Terminal - SistemaJuanchOS')
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            QWidget {
                background-color: #000000;
            }
        """)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Área de texto para la salida
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #1a1a1a;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #333333;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        layout.addWidget(self.text_area)

        # Línea de entrada
        input_layout = QHBoxLayout()
        
        # Etiqueta del prompt
        self.prompt_label = QLabel("$ ")
        self.prompt_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                background-color: transparent;
            }
        """)
        input_layout.addWidget(self.prompt_label)

        # Campo de entrada
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                border: none;
            }
        """)
        self.input_line.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.input_line)
        layout.addLayout(input_layout)

        # Centra la ventana
        self.center_window()

    def center_window(self):
        """
        Centra la ventana de la terminal en la pantalla.
        """
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def show_welcome_message(self):
        """
        Muestra el mensaje de bienvenida y la lista de comandos disponibles.
        """
        welcome = """
        Bienvenido a la Terminal de SistemaJuanchOS
        -----------------------------------------
        Comandos disponibles:
        - help: Muestra esta ayuda
        - mkdir: Crea un directorio
        - cd: Cambia de directorio
        - ls: Lista archivos
        - touch: Crea un archivo
        - cat: Muestra contenido de archivo
        - echo: Escribe en archivo
        - rm: Elimina archivo
        - pwd: Muestra directorio actual
        - exit: Cierra la terminal
        """
        self.append_output(welcome)

    def execute_command(self):
        """
        Ejecuta el comando ingresado por el usuario.
        Procesa el comando y muestra la salida en el área de texto.
        """
        command = self.input_line.text().strip()
        self.input_line.clear()
        
        if not command:
            return

        self.append_output(f"$ {command}")
        
        # Verifica que los gestores del sistema estén disponibles
        if not self.user_manager or not self.user_manager.file_system:
            self.append_output("Error: Sistema de archivos no disponible")
            return
            
        # Ejecuta el comando y muestra el resultado
        result = self.command_interface.execute_command(command)
        
        if result:
            self.append_output(result)
            if result == "exit":
                self.close()

    def append_output(self, text):
        """
        Agrega texto al área de salida.
        
        Args:
            text: Texto a agregar
        """
        self.text_area.append(text)
        self.text_area.moveCursor(QTextCursor.End)

    def closeEvent(self, event):
        """
        Maneja el evento de cierre de la ventana.
        Limpia los recursos antes de cerrar.
        
        Args:
            event: Evento de cierre
        """
        self.command_interface.cleanup()
        event.accept() 