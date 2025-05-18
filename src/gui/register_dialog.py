#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

class RegisterDialog(QDialog):
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Registro - SistemaJuanchOS')
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #333;
                border-radius: 5px;
                background-color: #2a2a2a;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #00ff00;
            }
            QPushButton {
                padding: 10px;
                background-color: #00ff00;
                color: black;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Título
        title = QLabel('Registro de Usuario')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Formulario
        self.setup_form(layout)
        
        # Botones
        self.setup_buttons(layout)

    def setup_form(self, layout):
        # Usuario
        username_label = QLabel("Usuario:")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese un nombre de usuario")
        layout.addWidget(self.username_input)
        
        # Contraseña
        password_label = QLabel("Contraseña:")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese una contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Confirmar contraseña
        confirm_label = QLabel("Confirmar Contraseña:")
        layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirme su contraseña")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_input)

    def setup_buttons(self, layout):
        button_layout = QHBoxLayout()
        
        self.register_button = QPushButton("Registrar")
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()
        
        # Validaciones
        if not username or not password or not confirm:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "Error", "El nombre de usuario debe tener al menos 3 caracteres")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        try:
            if self.user_manager.register_user(username, password):
                QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "El usuario ya existe")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar usuario: {str(e)}") 