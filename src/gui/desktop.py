#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Escritorio del Sistema Operativo
=========================================

Este módulo implementa la interfaz gráfica del escritorio del sistema operativo,
incluyendo:
- Menú de inicio
- Iconos del escritorio
- Barra de tareas
- Fondo dinámico
- Accesibilidad con texto a voz

Clases:
--------
- Desktop: Ventana principal del escritorio
- StartMenu: Menú de inicio del sistema
- DesktopIcon: Iconos del escritorio con funcionalidad de texto a voz
"""

# Importación de módulos de Qt para la interfaz gráfica
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QMessageBox, QDesktopWidget,
                           QFrame, QMenu, QAction, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter

# Importación de módulos adicionales
import cv2
from datetime import datetime
import os
import sys
import subprocess
import pyttsx3

# Importación de módulos locales
from core.user_manager import UserManager
from gui.terminal_window import TerminalWindow

class StartMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        self.setMinimumHeight(400)
        self.setMaximumHeight(600)
        
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 40, 40, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }
            QPushButton {
                text-align: left;
                padding: 10px;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                background-color: rgba(60, 60, 60, 0.4);
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 0.4);
            }
            QLabel {
                color: white;
                font-size: 14px;
                background-color: rgba(60, 60, 60, 0.4);
            }
            QLabel#logoLabel {
                background-color: transparent;
            }
            QScrollArea {
                border: none;
                background-color: rgba(40, 40, 40, 0.4);
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0.3);
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QWidget {
                background-color: rgba(40, 40, 40, 0.4);
            }
        """)
        
        self.setup_ui()
        self.hide()

    def setup_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Logo
        self.setup_logo(layout)
        
        # Separador
        self.add_separator(layout)
        
        # Aplicaciones
        apps_label = QLabel("Aplicaciones")
        layout.addWidget(apps_label)
        
        # Botones de aplicaciones
        self.setup_app_buttons(layout)
        
        layout.addStretch()
        
        # Separador
        self.add_separator(layout)
        
        # Botones de sistema
        self.setup_system_buttons(layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(main_widget)
        scroll.setWidgetResizable(True)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def setup_logo(self, layout):
        logo_label = QLabel()
        logo_label.setObjectName("logoLabel")
        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
        if os.path.exists(logo_path):
            original_pixmap = QPixmap(logo_path)
            rounded_pixmap = self.create_rounded_pixmap(original_pixmap)
            logo_label.setPixmap(rounded_pixmap.scaled(280, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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

    def add_separator(self, layout):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        layout.addWidget(separator)

    def setup_app_buttons(self, layout):
        apps = [
            ("Terminal", None),
            ("Calculadora", ["calc.exe"] if os.name == 'nt' else ["gnome-calculator"]),
            ("Explorador", ["explorer.exe"] if os.name == 'nt' else ["nautilus"])
        ]
        
        for name, command in apps:
            btn = QPushButton(name)
            if name == "Terminal":
                btn.clicked.connect(self.open_terminal)
            else:
                btn.clicked.connect(lambda checked, cmd=command: self.run_app(cmd))
            layout.addWidget(btn)

    def setup_system_buttons(self, layout):
        user_btn = QPushButton("Usuario")
        user_btn.clicked.connect(self.show_user_menu)
        layout.addWidget(user_btn)
        
        power_btn = QPushButton("Apagar")
        power_btn.clicked.connect(self.show_power_menu)
        layout.addWidget(power_btn)

    def open_terminal(self):
        if not hasattr(self.parent(), 'user_manager'):
            QMessageBox.critical(self, "Error", "No se pudo acceder al gestor de usuarios")
            return
        terminal = TerminalWindow(self.parent().user_manager, self.parent())
        terminal.show()
        self.hide()

    def show_user_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(0, 0, 0, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QMenu::item {
                color: white;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        logout = QAction("Cerrar Sesión", self)
        logout.triggered.connect(self.logout)
        menu.addAction(logout)
        
        menu.exec_(self.mapToGlobal(QPoint(0, self.height() - 50)))

    def show_power_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(0, 0, 0, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QMenu::item {
                color: white;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        shutdown = QAction("Apagar", self)
        shutdown.triggered.connect(self.shutdown_system)
        menu.addAction(shutdown)
        
        menu.exec_(self.mapToGlobal(QPoint(0, self.height() - 50)))

    def logout(self):
        reply = QMessageBox.question(self, 'Cerrar Sesión',
                                   '¿Está seguro que desea cerrar sesión?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.parent().close()

    def shutdown_system(self):
        reply = QMessageBox.question(self, 'Apagar',
                                   '¿Está seguro que desea apagar el sistema?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.parent().close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        logo_label = self.findChild(QLabel, "logoLabel")
        if logo_label and logo_label.pixmap():
            new_width = self.width() - 20
            new_height = int(new_width * 0.357)
            logo_label.setPixmap(logo_label.pixmap().scaled(
                new_width, new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

    def run_app(self, command):
        try:
            if os.name == 'nt':  # Windows
                if command[0] == "calc.exe":
                    subprocess.Popen(["calc.exe"], shell=True)
                elif command[0] == "explorer.exe":
                    subprocess.Popen(["explorer.exe"], shell=True)
            else:  # Linux/Unix
                subprocess.Popen(command)
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo ejecutar la aplicación: {str(e)}")

class DesktopIcon(QWidget):
    def __init__(self, name, icon_path, command, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 100)
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
            QLabel {
                color: white;
                background-color: transparent;
            }
            QWidget:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }
        """)
        
        self.name = name
        self.icon_path = icon_path
        self.command = command
        self.setup_ui(name, icon_path, command)
        self.setup_tooltip()
        
        # Inicializar el motor de texto a voz
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Obtener las voces disponibles
        voices = self.engine.getProperty('voices')
        # Buscar una voz en español si está disponible
        for voice in voices:
            if 'spanish' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Timer para el texto a voz
        self.speech_timer = QTimer()
        self.speech_timer.setSingleShot(True)
        self.speech_timer.timeout.connect(self.speak_text)
        self.current_text = ""

    def setup_ui(self, name, icon_path, command):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)
        
        # Icono
        icon_label = QLabel()
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            pixmap = icon.pixmap(QSize(48, 48))
            icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Texto
        text_label = QLabel(name)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: white;")
        layout.addWidget(text_label)
        
        self.mousePressEvent = self.on_click

    def on_click(self, event):
        try:
            if self.command[0] == "terminal":
                if not hasattr(self.parent(), 'user_manager'):
                    QMessageBox.critical(self, "Error", "No se pudo acceder al gestor de usuarios")
                    return
                terminal = TerminalWindow(self.parent().user_manager, self.parent())
                terminal.show()
            else:
                subprocess.Popen(self.command)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo ejecutar la aplicación: {str(e)}")

    def setup_tooltip(self):
        if self.command[0] == "terminal":
            self.setToolTip("Terminal del Sistema\nComandos disponibles:\n- help: Muestra ayuda\n- mkdir: Crea directorio\n- cd: Cambia directorio\n- ls: Lista archivos\n- touch: Crea archivo\n- cat: Lee archivo\n- echo: Escribe en archivo\n- rm: Elimina archivo\n- pwd: Muestra directorio actual")
        elif self.command[0] == "calc.exe":
            self.setToolTip("Calculadora de JuanchOs\nAbre la calculadora del sistema")
        elif self.command[0] == "explorer.exe":
            self.setToolTip("Explorador de JuanchOs\nAbre el explorador de archivos del sistema")
        else:
            self.setToolTip(f"Aplicación: {self.name}")

    def speak_text(self):
        try:
            self.engine.say(self.current_text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error al reproducir texto: {str(e)}")
    
    def enterEvent(self, event):
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }
            QLabel {
                color: white;
                background-color: transparent;
            }
        """)
        
        if self.command[0] == "terminal":
            self.current_text = f"Terminal del sistema."
        elif self.command[0] == "calc.exe":
            self.current_text = "Calculadora de JuanchOs"
        elif self.command[0] == "explorer.exe":
            self.current_text = "Explorador de JuanchOs"
        else:
            self.current_text = f"Aplicación {self.name}"
        
        self.speech_timer.start(100)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
            QLabel {
                color: white;
                background-color: transparent;
            }
            QWidget:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }
        """)
        super().leaveEvent(event)

class Desktop(QMainWindow):
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.background_label = None
        self.video_capture = None
        self.start_menu = None
        self.desktop_icons = []
        self.init_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def init_ui(self):
        self.setWindowTitle('SistemaJuanchOS - Desktop')
        self.setFixedSize(1800, 1000)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Fondo
        self.setup_background(layout)
        
        # Barra de tareas
        self.setup_taskbar(layout)
        
        # Menú de inicio
        self.start_menu = StartMenu(self)
        self.start_menu.hide()

        # Iconos del escritorio
        self.setup_desktop_icons()
        
        # Centrar ventana
        self.center()

    def setup_background(self, layout):
        self.background_label = QLabel()
        self.background_label.setStyleSheet("background-color: #1a1a1a;")
        
        background_path = os.path.join(os.path.dirname(__file__), 'assets', 'fondo.mp4')
        image_path = os.path.join(os.path.dirname(__file__), 'assets', 'wallpaper.jpg')
        
        if os.path.exists(background_path):
            try:
                self.setup_video_background(background_path)
            except Exception as e:
                print(f"Error al configurar el video de fondo: {e}")
                self.background_label.setStyleSheet("background-color: #1a1a1a;")
        elif os.path.exists(image_path):
            try:
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
                else:
                    print("Error: No se pudo cargar la imagen de fondo")
                    self.background_label.setStyleSheet("background-color: #1a1a1a;")
            except Exception as e:
                print(f"Error al cargar la imagen de fondo: {e}")
                self.background_label.setStyleSheet("background-color: #1a1a1a;")
        else:
            print("No se encontraron archivos de fondo. Usando color sólido.")
            self.background_label.setStyleSheet("background-color: #1a1a1a;")
        
        layout.addWidget(self.background_label)

    def setup_taskbar(self, layout):
        taskbar = QFrame()
        taskbar.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.5);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            QPushButton {
                padding: 8px;
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
        """)
        taskbar_layout = QHBoxLayout(taskbar)
        
        # Botón de inicio
        start_button = QPushButton()
        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            start_button.setIcon(QIcon(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        start_button.setIconSize(QSize(32, 32))
        start_button.clicked.connect(self.toggle_start_menu)
        taskbar_layout.addWidget(start_button)
        
        # Área de notificaciones
        notification_area = QFrame()
        notification_area.setStyleSheet("background-color: transparent;")
        notification_layout = QHBoxLayout(notification_area)
        
        self.time_label = QLabel()
        self.date_label = QLabel()
        self.update_time()
        notification_layout.addWidget(self.time_label)
        notification_layout.addWidget(self.date_label)
        
        taskbar_layout.addWidget(notification_area)
        layout.addWidget(taskbar)

    def setup_video_background(self, video_path):
        try:
            self.video_capture = cv2.VideoCapture(video_path)
            if not self.video_capture.isOpened():
                raise Exception("No se pudo abrir el video")

            self.video_timer = QTimer(self)
            self.video_timer.timeout.connect(self.update_video_frame)
            self.video_timer.start(30)
            print("Video de fondo iniciado correctamente")
        except Exception as e:
            print(f"Error al configurar el video de fondo: {e}")
            if self.video_capture:
                self.video_capture.release()
            self.background_label.setStyleSheet("background-color: #1a1a1a;")

    def update_video_frame(self):
        if self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width(), self.height()))
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.background_label.setPixmap(pixmap)
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def setup_desktop_icons(self):
        apps = [
            {
                "name": "Terminal",
                "icon": os.path.join(os.path.dirname(__file__), 'assets', 'terminal.png'),
                "command": ["terminal"]
            },
            {
                "name": "Calculadora",
                "icon": os.path.join(os.path.dirname(__file__), 'assets', 'calculator.png'),
                "command": ["calc.exe"] if os.name == 'nt' else ["gnome-calculator"]
            },
            {
                "name": "Explorador",
                "icon": os.path.join(os.path.dirname(__file__), 'assets', 'explorer.png'),
                "command": ["explorer.exe"] if os.name == 'nt' else ["nautilus"]
            }
        ]
        
        for i, app in enumerate(apps):
            icon = DesktopIcon(app["name"], app["icon"], app["command"], self)
            row = i // 4
            col = i % 4
            x = 20 + (col * 100)
            y = 20 + (row * 120)
            icon.move(x, y)
            icon.show()
            self.desktop_icons.append(icon)

    def toggle_start_menu(self):
        if self.start_menu.isVisible():
            self.start_menu.hide()
        else:
            pos = self.mapToGlobal(QPoint(0, self.height() - self.start_menu.height() - 80))
            self.start_menu.move(pos)
            self.start_menu.show()
            self.start_menu.raise_()

    def mousePressEvent(self, event):
        if self.start_menu and self.start_menu.isVisible():
            if not self.start_menu.geometry().contains(event.globalPos()):
                self.start_menu.hide()
        super().mousePressEvent(event)

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")
        if hasattr(self, 'time_label'):
            self.time_label.setText(current_time)
        if hasattr(self, 'date_label'):
            self.date_label.setText(current_date)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.setFixedSize(self.size())
        
        if self.video_capture and self.video_capture.isOpened():
            self.update_video_frame()
        
        if self.background_label.pixmap():
            self.background_label.setPixmap(
                self.background_label.pixmap().scaled(
                    self.size(), Qt.KeepAspectRatioByExpanding
                )
            )
        
        if self.start_menu and self.start_menu.isVisible():
            pos = self.mapToGlobal(QPoint(0, self.height() - self.start_menu.height() - 80))
            self.start_menu.move(pos) 