#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Sistema de Archivos del Sistema Operativo
================================================

Este módulo implementa el sistema de archivos del sistema operativo,
incluyendo:
- Gestión de archivos y directorios
- Operaciones CRUD
- Permisos de acceso
- Navegación del sistema de archivos

Clases:
--------
- FileSystem: Sistema principal de archivos
- File: Clase para representar archivos
- Directory: Clase para representar directorios
"""

import os
import json
from datetime import datetime

class File:
    """
    Representa un archivo en el sistema de archivos.
    
    Atributos:
        name: Nombre del archivo
        content: Contenido del archivo
        created_at: Fecha de creación
        modified_at: Fecha de última modificación
        size: Tamaño del archivo
        permissions: Permisos de acceso
    
    Métodos:
        read: Lee el contenido del archivo
        write: Escribe contenido en el archivo
        delete: Elimina el archivo
        get_info: Obtiene información del archivo
    """
    
    def __init__(self, name, content=""):
        self.name = name
        self.content = content
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.size = len(content)
        self.permissions = "rw-r--r--"

class Directory:
    """
    Representa un directorio en el sistema de archivos.
    
    Atributos:
        name: Nombre del directorio
        parent: Directorio padre
        children: Diccionario de archivos y subdirectorios
        created_at: Fecha de creación
        modified_at: Fecha de última modificación
        permissions: Permisos de acceso
    
    Métodos:
        add_child: Agrega un archivo o subdirectorio
        remove_child: Elimina un archivo o subdirectorio
        get_child: Obtiene un archivo o subdirectorio
        list_contents: Lista el contenido del directorio
    """
    
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.permissions = "rwxr-xr-x"

class FileSystem:
    """
    Implementa el sistema de archivos del sistema operativo.
    
    Atributos:
        root: Directorio raíz
        current_dir: Directorio actual
        file_system_path: Ruta al archivo de sistema de archivos
    
    Métodos:
        create_directory: Crea un directorio
        create_file: Crea un archivo
        delete_file: Elimina un archivo
        read_file: Lee un archivo
        write_file: Escribe en un archivo
        list_directory: Lista el contenido de un directorio
        change_directory: Cambia el directorio actual
        get_current_directory: Obtiene el directorio actual
        save_state: Guarda el estado del sistema de archivos
        load_state: Carga el estado del sistema de archivos
    """
    
    def __init__(self):
        self.root = Directory("/")
        self.current_dir = self.root
        self.file_system_path = "file_system.json"
        self.load_state()

