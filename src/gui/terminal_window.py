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

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTextEdit,
                           QLineEdit, QPushButton, QHBoxLayout, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QTextCursor, QColor, QTextCharFormat
import sys
import os
from kernel.file_system import FileSystem
from kernel.process_manager import ProcessManager
from kernel.memory_manager import MemoryManager
from shell.command_interface import CommandInterface

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
    
    Métodos:
        init_ui: Inicializa la interfaz de usuario
        setup_terminal: Configura la terminal
        execute_command: Ejecuta un comando
        update_prompt: Actualiza el prompt
        handle_key_press: Maneja eventos de teclado
        show_error: Muestra mensajes de error
    """
    
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.file_system = FileSystem()
        self.process_manager = ProcessManager()
        self.memory_manager = MemoryManager()
        self.command_interface = CommandInterface(
            self.file_system,
            self.process_manager,
            self.memory_manager,
            self.user_manager
        )
        self.command_history = []
        self.current_history_index = -1
        self.prompt = "$ "
        self.current_dir = "/"
        self.init_ui()
        self.show_welcome_message()

    def init_ui(self):
        self.setWindowTitle('Terminal - SistemaJuanchOS')
        self.setFixedSize(800, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Área de texto
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                border: none;
            }
        """)
        layout.addWidget(self.text_area)

        # Línea de entrada
        input_layout = QHBoxLayout()
        self.prompt_label = QLabel("$ ")
        self.prompt_label.setStyleSheet("color: #00ff00;")
        input_layout.addWidget(self.prompt_label)

        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                border: none;
            }
        """)
        self.input_line.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.input_line)
        layout.addLayout(input_layout)

        # Centrar ventana
        self.center_window()

    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def show_welcome_message(self):
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
        command = self.input_line.text().strip()
        self.input_line.clear()
        
        if not command:
            return

        self.append_output(f"$ {command}")
        
        # Verificar que los gestores del sistema estén disponibles
        if not self.user_manager or not self.user_manager.file_system:
            self.append_output("Error: Sistema de archivos no disponible")
            return
            
        result = self.command_interface.execute_command(command)
        
        if result:
            self.append_output(result)
            if result == "exit":
                self.close()

    def append_output(self, text):
        self.text_area.append(text)
        self.text_area.moveCursor(QTextCursor.End)

    def closeEvent(self, event):
        self.command_interface.cleanup()
        event.accept() 