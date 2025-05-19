#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Interfaz de Comandos del Sistema Operativo
=================================================

Este módulo implementa la interfaz de comandos del sistema operativo,
incluyendo:
- Procesamiento de comandos
- Gestión de archivos
- Gestión de procesos
- Gestión de memoria
- Autenticación de usuarios

Clases:
--------
- CommandInterface: Interfaz principal de comandos
"""

# Importación de módulos del sistema
import os
import sys
import shutil
from datetime import datetime

from .file_system import FileSystem
from .process_manager import ProcessManager
from .memory_manager import MemoryManager
from .user_manager import UserManager

class CommandInterface:
    """
    Implementa la interfaz de comandos del sistema operativo.
    
    Atributos:
        file_system: Sistema de archivos
        process_manager: Gestor de procesos
        memory_manager: Gestor de memoria
        user_manager: Gestor de usuarios
        current_dir: Directorio actual
        commands: Diccionario de comandos disponibles
    """
    
    def __init__(self, file_system, process_manager, memory_manager, user_manager):
        """
        Inicializa la interfaz de comandos.
        
        Args:
            file_system: Sistema de archivos
            process_manager: Gestor de procesos
            memory_manager: Gestor de memoria
            user_manager: Gestor de usuarios
        """
        self.file_system = file_system
        self.process_manager = process_manager
        self.memory_manager = memory_manager
        self.user_manager = user_manager
        self.current_dir = "/"
        
        # Registra los comandos disponibles
        self.commands = {
            "help": self.help,
            "mkdir": self.mkdir,
            "cd": self.cd,
            "ls": self.ls,
            "touch": self.touch,
            "cat": self.cat,
            "echo": self.echo,
            "rm": self.rm,
            "pwd": self.pwd,
            "exit": self.exit
        }

    def execute_command(self, command):
        """
        Ejecuta un comando del sistema.
        
        Args:
            command: Comando a ejecutar
            
        Returns:
            str: Resultado de la ejecución del comando
        """
        try:
            # Divide el comando en partes
            parts = command.split()
            if not parts:
                return ""
                
            cmd = parts[0].lower()
            args = parts[1:]
            
            # Verifica si el comando existe
            if cmd in self.commands:
                return self.commands[cmd](*args)
            else:
                return f"Comando no encontrado: {cmd}"
                
        except Exception as e:
            return f"Error al ejecutar el comando: {str(e)}"

    def help(self, *args):
        """
        Muestra la ayuda de los comandos disponibles.
        
        Returns:
            str: Lista de comandos y su descripción
        """
        help_text = """
        Comandos disponibles:
        - help: Muestra esta ayuda
        - mkdir <nombre>: Crea un directorio
        - cd <ruta>: Cambia de directorio
        - ls [ruta]: Lista archivos
        - touch <nombre>: Crea un archivo
        - cat <archivo>: Muestra contenido de archivo
        - echo <texto> > <archivo>: Escribe en archivo
        - rm <archivo>: Elimina archivo
        - pwd: Muestra directorio actual
        - exit: Cierra la terminal
        """
        return help_text

    def mkdir(self, *args):
        """
        Crea un nuevo directorio.
        
        Args:
            *args: Nombre del directorio a crear
            
        Returns:
            str: Mensaje de éxito o error
        """
        if not args:
            return "Uso: mkdir <nombre>"
            
        dir_name = args[0]
        try:
            self.file_system.create_directory(self.current_dir, dir_name)
            return f"Directorio creado: {dir_name}"
        except Exception as e:
            return f"Error al crear directorio: {str(e)}"

    def cd(self, *args):
        """
        Cambia el directorio actual.
        
        Args:
            *args: Ruta del directorio destino
            
        Returns:
            str: Mensaje de éxito o error
        """
        if not args:
            return "Uso: cd <ruta>"
            
        path = args[0]
        try:
            new_dir = self.file_system.change_directory(self.current_dir, path)
            self.current_dir = new_dir
            return f"Directorio actual: {new_dir}"
        except Exception as e:
            return f"Error al cambiar directorio: {str(e)}"

    def ls(self, *args):
        """
        Lista los archivos y directorios.
        
        Args:
            *args: Ruta opcional a listar
            
        Returns:
            str: Lista de archivos y directorios
        """
        path = args[0] if args else self.current_dir
        try:
            items = self.file_system.list_directory(path)
            if not items:
                return "Directorio vacío"
                
            result = []
            for item in items:
                if item.is_directory:
                    result.append(f"[DIR] {item.name}")
                else:
                    result.append(f"[FILE] {item.name}")
            return "\n".join(result)
        except Exception as e:
            return f"Error al listar directorio: {str(e)}"

    def touch(self, *args):
        """
        Crea un nuevo archivo.
        
        Args:
            *args: Nombre del archivo a crear
            
        Returns:
            str: Mensaje de éxito o error
        """
        if not args:
            return "Uso: touch <nombre>"
            
        file_name = args[0]
        try:
            self.file_system.create_file(self.current_dir, file_name)
            return f"Archivo creado: {file_name}"
        except Exception as e:
            return f"Error al crear archivo: {str(e)}"

    def cat(self, *args):
        """
        Muestra el contenido de un archivo.
        
        Args:
            *args: Nombre del archivo a mostrar
            
        Returns:
            str: Contenido del archivo o mensaje de error
        """
        if not args:
            return "Uso: cat <archivo>"
            
        file_name = args[0]
        try:
            content = self.file_system.read_file(self.current_dir, file_name)
            return content
        except Exception as e:
            return f"Error al leer archivo: {str(e)}"

    def echo(self, *args):
        """
        Escribe texto en un archivo.
        
        Args:
            *args: Texto y nombre del archivo
            
        Returns:
            str: Mensaje de éxito o error
        """
        if len(args) < 3 or args[-2] != ">":
            return "Uso: echo <texto> > <archivo>"
            
        text = " ".join(args[:-2])
        file_name = args[-1]
        try:
            self.file_system.write_file(self.current_dir, file_name, text)
            return f"Texto escrito en: {file_name}"
        except Exception as e:
            return f"Error al escribir archivo: {str(e)}"

    def rm(self, *args):
        """
        Elimina un archivo o directorio.
        
        Args:
            *args: Nombre del archivo o directorio a eliminar
            
        Returns:
            str: Mensaje de éxito o error
        """
        if not args:
            return "Uso: rm <archivo>"
            
        name = args[0]
        try:
            self.file_system.delete(self.current_dir, name)
            return f"Eliminado: {name}"
        except Exception as e:
            return f"Error al eliminar: {str(e)}"

    def pwd(self, *args):
        """
        Muestra el directorio actual.
        
        Returns:
            str: Ruta del directorio actual
        """
        return self.current_dir

    def exit(self, *args):
        """
        Cierra la terminal.
        
        Returns:
            str: Mensaje de despedida
        """
        return "exit"

    def cleanup(self):
        """
        Limpia los recursos antes de cerrar.
        """
        if self.file_system:
            self.file_system.save() 