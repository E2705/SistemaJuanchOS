#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import hashlib
import secrets
from typing import Dict, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

@dataclass
class User:
    """Clase que representa un usuario del sistema."""
    username: str
    password_hash: str
    salt: str
    is_admin: bool = False
    created_at: datetime = None
    last_login: Optional[datetime] = None
    home_directory: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.home_directory is None:
            self.home_directory = os.path.join(os.path.expanduser("~"), self.username)

    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña es correcta."""
        hash_obj = hashlib.sha256()
        hash_obj.update((password + self.salt).encode())
        return hash_obj.hexdigest() == self.password_hash

    def to_dict(self) -> Dict:
        """Convierte el usuario a un diccionario."""
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'is_admin': self.is_admin,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'last_login': self.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.last_login else None,
            'home_directory': self.home_directory
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Crea un usuario desde un diccionario."""
        return cls(
            username=data['username'],
            password_hash=data['password_hash'],
            salt=data['salt'],
            is_admin=data['is_admin'],
            created_at=datetime.strptime(data['created_at'], "%Y-%m-%d %H:%M:%S"),
            last_login=datetime.strptime(data['last_login'], "%Y-%m-%d %H:%M:%S") if data['last_login'] else None,
            home_directory=data['home_directory']
        )

class UserManager:
    """Gestor de usuarios del sistema."""
    def __init__(self, users_file: str = "users.json"):
        """
        Inicializa el gestor de usuarios.
        
        Args:
            users_file: Ruta al archivo de usuarios.
        """
        self.users_file = users_file
        self.users: Dict[str, User] = {}
        self.current_user: Optional[User] = None
        self.file_system = None
        self.process_manager = None
        self.memory_manager = None
        self.load_users()

    def set_managers(self, file_system, process_manager, memory_manager):
        """Establece los gestores del sistema."""
        self.file_system = file_system
        self.process_manager = process_manager
        self.memory_manager = memory_manager

    def load_users(self) -> bool:
        """Carga los usuarios desde el archivo."""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    data = json.load(f)
                    self.users = {
                        username: User.from_dict(user_data)
                        for username, user_data in data.items()
                    }
            return True
        except Exception as e:
            print(f"Error al cargar usuarios: {str(e)}")
            return False

    def save_users(self) -> bool:
        """Guarda los usuarios en el archivo."""
        try:
            data = {
                username: user.to_dict()
                for username, user in self.users.items()
            }
            with open(self.users_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar usuarios: {str(e)}")
            return False

    def create_user(self, username: str, password: str, is_admin: bool = False) -> Tuple[bool, str]:
        """
        Crea un nuevo usuario.
        
        Args:
            username: Nombre de usuario.
            password: Contraseña.
            is_admin: Si el usuario es administrador.
            
        Returns:
            Tupla (éxito, mensaje).
        """
        if username in self.users:
            return False, "El usuario ya existe"

        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"

        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"

        # Generar salt y hash de la contraseña
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256()
        hash_obj.update((password + salt).encode())
        password_hash = hash_obj.hexdigest()

        # Crear usuario
        user = User(
            username=username,
            password_hash=password_hash,
            salt=salt,
            is_admin=is_admin
        )

        # Crear directorio home
        try:
            os.makedirs(user.home_directory, exist_ok=True)
        except Exception as e:
            return False, f"Error al crear directorio home: {str(e)}"

        self.users[username] = user
        if self.save_users():
            return True, "Usuario creado correctamente"
        return False, "Error al guardar el usuario"

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Inicia sesión con un usuario.
        
        Args:
            username: Nombre de usuario.
            password: Contraseña.
            
        Returns:
            Tupla (éxito, mensaje).
        """
        if username not in self.users:
            return False, "Usuario o contraseña incorrectos"

        user = self.users[username]
        if not user.verify_password(password):
            return False, "Usuario o contraseña incorrectos"

        user.last_login = datetime.now()
        self.current_user = user
        self.save_users()
        return True, "Inicio de sesión exitoso"

    def logout(self) -> None:
        """Cierra la sesión del usuario actual."""
        self.current_user = None

    def get_current_user(self) -> Optional[Dict]:
        """Obtiene información del usuario actual."""
        if self.current_user is None:
            return None
        return {
            'username': self.current_user.username,
            'is_admin': self.current_user.is_admin,
            'created_at': self.current_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'last_login': self.current_user.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.current_user.last_login else None,
            'home_directory': self.current_user.home_directory
        } 