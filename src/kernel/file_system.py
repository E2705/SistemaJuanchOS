#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional

class FileSystem:
    def __init__(self):
        self.current_directory = os.path.expanduser("~")
        self.root_directory = os.path.expanduser("~")
        self.initialize_system()

    def initialize_system(self):
        """Inicializa el sistema de archivos con directorios básicos."""
        try:
            # Crear directorios del sistema si no existen
            system_dirs = ['/bin', '/etc', '/home', '/tmp', '/var']
            for dir_path in system_dirs:
                full_path = os.path.join(self.root_directory, dir_path.lstrip('/'))
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
        except Exception as e:
            print(f"Error al inicializar el sistema de archivos: {str(e)}")

    def get_current_directory(self) -> str:
        """Retorna el directorio actual."""
        return self.current_directory

    def change_directory(self, path: str) -> bool:
        """Cambia el directorio actual."""
        try:
            new_path = self.resolve_path(path)
            if not os.path.exists(new_path) or not os.path.isdir(new_path):
                return False
            self.current_directory = new_path
            return True
        except Exception:
            return False

    def list_directory(self, path: str = None) -> List[Dict[str, str]]:
        """Lista el contenido de un directorio."""
        try:
            target_path = self.resolve_path(path) if path else self.current_directory
            if not os.path.exists(target_path) or not os.path.isdir(target_path):
                return []

            items = []
            for item in os.listdir(target_path):
                item_path = os.path.join(target_path, item)
                items.append({
                    'name': item,
                    'type': 'directory' if os.path.isdir(item_path) else 'file',
                    'size': self.get_size(item_path)
                })
            return items
        except Exception:
            return []

    def create_directory(self, path: str) -> bool:
        """Crea un nuevo directorio."""
        try:
            full_path = self.resolve_path(path)
            if os.path.exists(full_path):
                return False
            os.makedirs(full_path)
            return True
        except Exception:
            return False

    def create_file(self, path: str) -> bool:
        """Crea un nuevo archivo."""
        try:
            full_path = self.resolve_path(path)
            if os.path.exists(full_path):
                return False
            with open(full_path, 'w') as f:
                pass
            return True
        except Exception:
            return False

    def read_file(self, path: str) -> Optional[str]:
        """Lee el contenido de un archivo."""
        try:
            full_path = self.resolve_path(path)
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                return None
            with open(full_path, 'r') as f:
                return f.read()
        except Exception:
            return None

    def write_file(self, path: str, content: str) -> bool:
        """Escribe contenido en un archivo."""
        try:
            full_path = self.resolve_path(path)
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                return False
            with open(full_path, 'w') as f:
                f.write(content)
            return True
        except Exception:
            return False

    def delete_file(self, path: str) -> bool:
        """Elimina un archivo o directorio."""
        try:
            full_path = self.resolve_path(path)
            if not os.path.exists(full_path):
                return False
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            return True
        except Exception:
            return False

    def resolve_path(self, path: str) -> str:
        """Resuelve una ruta relativa o absoluta."""
        if os.path.isabs(path):
            return os.path.normpath(path)
        return os.path.normpath(os.path.join(self.current_directory, path))

    def get_size(self, path: str) -> str:
        """Obtiene el tamaño de un archivo o directorio."""
        try:
            if os.path.isfile(path):
                size = os.path.getsize(path)
            else:
                size = sum(os.path.getsize(os.path.join(dirpath, filename))
                          for dirpath, dirnames, filenames in os.walk(path)
                          for filename in filenames)
            
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except Exception:
            return "0 B" 