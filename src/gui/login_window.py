#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Ventana de Inicio de Sesión
====================================

Este módulo implementa la interfaz gráfica de inicio de sesión del sistema operativo,
incluyendo:
- Formulario de inicio de sesión
- Validación de credenciales
- Manejo de errores
- Transición al escritorio

Clases:
--------
- LoginWindow: Ventana de inicio de sesión
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QMessageBox,
                           QDesktopWidget, QFrame)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPainter, QColor
import os
from gui.desktop import Desktop

class LoginWindow(QMainWindow):
    """
    Implementa la ventana de inicio de sesión del sistema operativo.
    
    Atributos:
        user_manager: Gestor de usuarios del sistema
        file_system: Sistema de archivos
        process_manager: Gestor de procesos
        memory_manager: Gestor de memoria
        username_input: Campo de entrada para el nombre de usuario
        password_input: Campo de entrada para la contraseña
        login_button: Botón de inicio de sesión
        status_label: Etiqueta de estado
        login_attempts: Contador de intentos de inicio de sesión
        lockout_timer: Timer para el bloqueo temporal
    """
    
    def __init__(self, user_manager, file_system, process_manager, memory_manager):
        super().__init__()
        self.user_manager = user_manager
        self.file_system = file_system
        self.process_manager = process_manager
        self.memory_manager = memory_manager
        self.login_attempts = 0
        self.lockout_timer = QTimer()
        self.lockout_timer.timeout.connect(self.reset_login_attempts)
        self.init_ui()
        self.center()

    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        self.setWindowTitle('SistemaJuanchOS - Login')
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: transparent;
            }
            QWidget#centralWidget {
                background-color: rgba(40, 40, 40, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 14px;
                background-color: transparent;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                background-color: rgba(60, 60, 60, 0.4);
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 255, 255, 0.3);
                background-color: rgba(80, 80, 80, 0.4);
            }
            QPushButton {
                padding: 10px;
                background-color: rgba(0, 123, 255, 0.4);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 123, 255, 0.6);
            }
            QPushButton:disabled {
                background-color: rgba(102, 102, 102, 0.4);
                color: rgba(153, 153, 153, 0.8);
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Logo
        self.setup_logo(layout)
        
        # Formulario de login
        self.setup_login_form(layout)
        
        # Botón de inicio de sesión
        self.setup_login_button(layout)

    def setup_logo(self, layout):
        """Configura el logo de la aplicación."""
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
        if os.path.exists(logo_path):
            original_pixmap = QPixmap(logo_path)
            rounded_pixmap = self.create_rounded_pixmap(original_pixmap)
            logo_label.setPixmap(rounded_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

    def create_rounded_pixmap(self, original_pixmap):
        mask = QPixmap(original_pixmap.size())
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, mask.width(), mask.height(), 50, 50)
        painter.end()
        
        rounded_pixmap = QPixmap(original_pixmap.size())
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(0, 0, original_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        painter.drawPixmap(0, 0, mask)
        painter.end()
        
        return rounded_pixmap

    def setup_login_form(self, layout):
        """
        Configura el formulario de inicio de sesión.
        
        Args:
            layout: Layout vertical para agregar los widgets
        """
        # Usuario
        username_label = QLabel("Usuario:")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su usuario")
        layout.addWidget(self.username_input)
        
        # Contraseña
        password_label = QLabel("Contraseña:")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

    def setup_login_button(self, layout):
        """Configura el botón de inicio de sesión."""
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)
        
        # Agregar espacio flexible
        layout.addStretch()

    def login(self):
        """Maneja el proceso de inicio de sesión."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            return
        
        try:
            if self.user_manager.login(username, password):
                self.open_desktop()
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar sesión: {str(e)}")

    def open_desktop(self):
        """Abre la ventana del escritorio después de un inicio de sesión exitoso."""
        self.desktop = Desktop(self.user_manager)
        self.desktop.show()
        self.close()

    def center(self):
        """Centra la ventana en la pantalla."""
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def reset_login_attempts(self):
        """Reinicia el contador de intentos de inicio de sesión."""
        self.login_attempts = 0
        self.lockout_timer.stop()

    def show_error(self, message):
        """Muestra un mensaje de error."""
        QMessageBox.critical(self, "Error", message) 