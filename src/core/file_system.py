#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Sistema de Archivos del Sistema Operativo
=================================================

Este módulo implementa el sistema de archivos del sistema operativo,
incluyendo:
- Gestión de archivos y directorios
- Operaciones de lectura/escritura
- Permisos y seguridad
- Persistencia de datos

Clases:
--------
- File: Representa un archivo
- Directory: Representa un directorio
- FileSystem: Sistema de archivos principal
"""

# Importación de módulos del sistema
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union

class File:
    """
    Representa un archivo en el sistema.
    
    Atributos:
        name: Nombre del archivo
        content: Contenido del archivo
        created_at: Fecha de creación
        modified_at: Fecha de modificación
        size: Tamaño en bytes
        permissions: Permisos del archivo
    """
    
    def __init__(self, name: str, content: str = ""):
        """
        Inicializa un nuevo archivo.
        
        Args:
            name: Nombre del archivo
            content: Contenido inicial del archivo
        """
        self.name = name
        self.content = content
        self.created_at = datetime.now()
        self.modified_at = self.created_at
        self.size = len(content)
        self.permissions = "rw-r--r--"

    def to_dict(self) -> Dict:
        """
        Convierte el archivo a un diccionario.
        
        Returns:
            Dict: Representación del archivo
        """
        return {
            "name": self.name,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "size": self.size,
            "permissions": self.permissions
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'File':
        """
        Crea un archivo desde un diccionario.
        
        Args:
            data: Datos del archivo
            
        Returns:
            File: Nueva instancia de archivo
        """
        file = cls(data["name"], data["content"])
        file.created_at = datetime.fromisoformat(data["created_at"])
        file.modified_at = datetime.fromisoformat(data["modified_at"])
        file.size = data["size"]
        file.permissions = data["permissions"]
        return file

class Directory:
    """
    Representa un directorio en el sistema.
    
    Atributos:
        name: Nombre del directorio
        created_at: Fecha de creación
        modified_at: Fecha de modificación
        items: Contenido del directorio
        permissions: Permisos del directorio
    """
    
    def __init__(self, name: str):
        """
        Inicializa un nuevo directorio.
        
        Args:
            name: Nombre del directorio
        """
        self.name = name
        self.created_at = datetime.now()
        self.modified_at = self.created_at
        self.items: Dict[str, Union[File, 'Directory']] = {}
        self.permissions = "rwxr-xr-x"

    def to_dict(self) -> Dict:
        """
        Convierte el directorio a un diccionario.
        
        Returns:
            Dict: Representación del directorio
        """
        return {
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "items": {
                name: item.to_dict() for name, item in self.items.items()
            },
            "permissions": self.permissions
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Directory':
        """
        Crea un directorio desde un diccionario.
        
        Args:
            data: Datos del directorio
            
        Returns:
            Directory: Nueva instancia de directorio
        """
        directory = cls(data["name"])
        directory.created_at = datetime.fromisoformat(data["created_at"])
        directory.modified_at = datetime.fromisoformat(data["modified_at"])
        directory.permissions = data["permissions"]
        
        for name, item_data in data["items"].items():
            if "content" in item_data:
                directory.items[name] = File.from_dict(item_data)
            else:
                directory.items[name] = Directory.from_dict(item_data)
                
        return directory

class FileSystem:
    """
    Implementa el sistema de archivos principal.
    
    Atributos:
        root: Directorio raíz
        current_path: Ruta actual
        data_file: Archivo de persistencia
    """
    
    def __init__(self, data_file: str = "filesystem.json"):
        """
        Inicializa el sistema de archivos.
        
        Args:
            data_file: Ruta del archivo de persistencia
        """
        self.root = Directory("/")
        self.current_path = "/"
        self.data_file = data_file
        self.load()

    def load(self):
        """
        Carga el sistema de archivos desde el archivo de persistencia.
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.root = Directory.from_dict(data)
        except Exception as e:
            print(f"Error al cargar sistema de archivos: {str(e)}")

    def save(self):
        """
        Guarda el sistema de archivos en el archivo de persistencia.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.root.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Error al guardar sistema de archivos: {str(e)}")

    def get_item(self, path: str) -> Optional[Union[File, Directory]]:
        """
        Obtiene un archivo o directorio por su ruta.
        
        Args:
            path: Ruta del item
            
        Returns:
            Union[File, Directory]: Item encontrado o None
        """
        if path == "/":
            return self.root
            
        parts = path.strip("/").split("/")
        current = self.root
        
        for part in parts:
            if part not in current.items:
                return None
            current = current.items[part]
            
        return current

    def create_file(self, directory: str, name: str, content: str = "") -> File:
        """
        Crea un nuevo archivo.
        
        Args:
            directory: Directorio donde crear
            name: Nombre del archivo
            content: Contenido inicial
            
        Returns:
            File: Archivo creado
            
        Raises:
            ValueError: Si el archivo ya existe
        """
        parent = self.get_item(directory)
        if not isinstance(parent, Directory):
            raise ValueError(f"Directorio no encontrado: {directory}")
            
        if name in parent.items:
            raise ValueError(f"Archivo ya existe: {name}")
            
        file = File(name, content)
        parent.items[name] = file
        parent.modified_at = datetime.now()
        self.save()
        return file

    def read_file(self, directory: str, name: str) -> str:
        """
        Lee el contenido de un archivo.
        
        Args:
            directory: Directorio del archivo
            name: Nombre del archivo
            
        Returns:
            str: Contenido del archivo
            
        Raises:
            ValueError: Si el archivo no existe
        """
        parent = self.get_item(directory)
        if not isinstance(parent, Directory):
            raise ValueError(f"Directorio no encontrado: {directory}")
            
        if name not in parent.items:
            raise ValueError(f"Archivo no encontrado: {name}")
            
        file = parent.items[name]
        if not isinstance(file, File):
            raise ValueError(f"No es un archivo: {name}")
            
        return file.content

    def write_file(self, directory: str, name: str, content: str):
        """
        Escribe contenido en un archivo.
        
        Args:
            directory: Directorio del archivo
            name: Nombre del archivo
            content: Contenido a escribir
            
        Raises:
            ValueError: Si el archivo no existe
        """
        parent = self.get_item(directory)
        if not isinstance(parent, Directory):
            raise ValueError(f"Directorio no encontrado: {directory}")
            
        if name not in parent.items:
            raise ValueError(f"Archivo no encontrado: {name}")
            
        file = parent.items[name]
        if not isinstance(file, File):
            raise ValueError(f"No es un archivo: {name}")
            
        file.content = content
        file.size = len(content)
        file.modified_at = datetime.now()
        parent.modified_at = file.modified_at
        self.save()

    def delete(self, directory: str, name: str):
        """
        Elimina un archivo o directorio.
        
        Args:
            directory: Directorio contenedor
            name: Nombre del item a eliminar
            
        Raises:
            ValueError: Si el item no existe
        """
        parent = self.get_item(directory)
        if not isinstance(parent, Directory):
            raise ValueError(f"Directorio no encontrado: {directory}")
            
        if name not in parent.items:
            raise ValueError(f"Item no encontrado: {name}")
            
        del parent.items[name]
        parent.modified_at = datetime.now()
        self.save()

    def create_directory(self, parent_dir: str, name: str) -> Directory:
        """
        Crea un nuevo directorio.
        
        Args:
            parent_dir: Directorio padre
            name: Nombre del directorio
            
        Returns:
            Directory: Directorio creado
            
        Raises:
            ValueError: Si el directorio ya existe
        """
        parent = self.get_item(parent_dir)
        if not isinstance(parent, Directory):
            raise ValueError(f"Directorio no encontrado: {parent_dir}")
            
        if name in parent.items:
            raise ValueError(f"Directorio ya existe: {name}")
            
        directory = Directory(name)
        parent.items[name] = directory
        parent.modified_at = datetime.now()
        self.save()
        return directory

    def list_directory(self, path: str) -> List[Union[File, Directory]]:
        """
        Lista el contenido de un directorio.
        
        Args:
            path: Ruta del directorio
            
        Returns:
            List[Union[File, Directory]]: Lista de items
            
        Raises:
            ValueError: Si el directorio no existe
        """
        directory = self.get_item(path)
        if not isinstance(directory, Directory):
            raise ValueError(f"Directorio no encontrado: {path}")
            
        return list(directory.items.values())

    def change_directory(self, current: str, target: str) -> str:
        """
        Cambia el directorio actual.
        
        Args:
            current: Directorio actual
            target: Directorio destino
            
        Returns:
            str: Nueva ruta
            
        Raises:
            ValueError: Si el directorio no existe
        """
        if target == "..":
            parts = current.strip("/").split("/")
            if len(parts) > 1:
                return "/" + "/".join(parts[:-1])
            return "/"
            
        if target.startswith("/"):
            new_path = target
        else:
            new_path = os.path.join(current, target)
            
        directory = self.get_item(new_path)
        if not isinstance(directory, Directory):
            raise ValueError(f"Directorio no encontrado: {target}")
            
        return new_path

