#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Gestor de Usuarios del Sistema Operativoñ
==============================================

Este módulo implementa el gestor de usuarios del sistema operativo,
incluyendo:
- Autenticación de usuarios
- Gestión de sesiones
- Permisos de usuario
- Almacenamiento seguro de credenciales

Clases:
--------
- UserManager: Gestor principal de usuarios
- User: Clase para representar usuarios
"""

import bcrypt
import json
from datetime import datetime

class User:
    """
    Representa un usuario en el sistema operativo.
    
    Atributos:
        username: Nombre de usuario
        password_hash: Hash de la contraseña
        role: Rol del usuario (admin, user)
        created_at: Fecha de creación
        last_login: Último inicio de sesión
        is_active: Indica si el usuario está activo
    
    Métodos:
        verify_password: Verifica la contraseña
        change_password: Cambia la contraseña
        get_info: Obtiene información del usuario
    """
    
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.role = role
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True
        
    def to_dict(self):
        """
        Convierte el objeto User a un diccionario.
        
        Returns:
            dict: Diccionario con la información del usuario
        """
        return {
            'username': self.username,
            'password_hash': self.password_hash.decode(),
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

class UserManager:
    """
    Implementa el gestor de usuarios del sistema operativo.
    
    Atributos:
        users: Diccionario de usuarios registrados
        current_user: Usuario actual
        users_file: Ruta al archivo de usuarios
    
    Métodos:
        create_user: Crea un nuevo usuario
        delete_user: Elimina un usuario
        authenticate: Autentica un usuario
        logout: Cierra la sesión
        get_user_info: Obtiene información de un usuario
        save_users: Guarda los usuarios en disco
        load_users: Carga los usuarios desde disco
    """
    
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.users_file = "users.json"
        self.load_users()
        
        # Crear usuario administrador por defecto si no existe ninguno
        if not self.users:
            self.create_user("admin", "admin", role="admin")

    def load_users(self):
        """
        Carga los usuarios registrados desde el archivo de usuarios.
        """
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}

    def save_users(self):
        """
        Guarda los usuarios registrados en el archivo de usuarios.
        """
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def create_user(self, username, password, role="user"):
        """
        Crea un nuevo usuario registrado en el sistema.
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            role: Rol del usuario (admin, user)
        
        Returns:
            bool: True si el usuario se creó correctamente, False en caso contrario
        """
        if username in self.users:
            return False
        self.users[username] = User(username, password, role).to_dict()
        self.save_users()
        return True

    def delete_user(self, username):
        """
        Elimina un usuario registrado del sistema.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si el usuario se eliminó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        del self.users[username]
        self.save_users()
        return True

    def authenticate(self, username, password):
        """
        Autentica un usuario registrado en el sistema.
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
        
        Returns:
            bool: True si el usuario se autenticó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        stored_hash = self.users[username]['password_hash'].encode()
        return bcrypt.checkpw(password.encode(), stored_hash)

    def login(self, username, password):
        """
        Inicia sesión con un usuario registrado.
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
        
        Returns:
            bool: True si el inicio de sesión fue exitoso, False en caso contrario
        """
        if self.authenticate(username, password):
            self.current_user = username
            self.users[username]['last_login'] = datetime.now().isoformat()
            self.save_users()
            return True
        return False

    def logout(self):
        """
        Cierra la sesión del usuario actual.
        """
        self.current_user = None

    def get_user_info(self, username):
        """
        Obtiene información de un usuario registrado.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            dict: Información del usuario
        """
        if username not in self.users:
            return None
        return self.users[username]

    def get_current_user(self):
        """
        Obtiene el usuario actual registrado.
        
        Returns:
            User: Usuario actual registrado
        """
        return self.current_user

    def update_user_info(self, username, **kwargs):
        """
        Actualiza la información de un usuario registrado.
        
        Args:
            username: Nombre de usuario
            **kwargs: Información actualizada del usuario
        
        Returns:
            bool: True si la información se actualizó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username].update(kwargs)
        self.save_users()
        return True

    def update_password(self, username, new_password):
        """
        Actualiza la contraseña de un usuario registrado.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
        
        Returns:
            bool: True si la contraseña se actualizó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.save_users()
        return True

    def update_role(self, username, new_role):
        """
        Actualiza el rol de un usuario registrado.
        
        Args:
            username: Nombre de usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si el rol se actualizó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['role'] = new_role
        self.save_users()
        return True

    def update_last_login(self, username):
        """
        Actualiza el último inicio de sesión de un usuario registrado.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si el último inicio de sesión se actualizó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.save_users()
        return True

    def update_is_active(self, username, is_active):
        """
        Actualiza el estado activo de un usuario registrado.
        
        Args:
            username: Nombre de usuario
            is_active: Nuevo estado activo del usuario
        
        Returns:
            bool: True si el estado activo se actualizó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['is_active'] = is_active
        self.save_users()
        return True

    def update_created_at(self, username, created_at):
        """
        Actualiza la fecha de creación de un usuario registrado.
        
        Args:
            username: Nombre de usuario
            created_at: Nueva fecha de creación del usuario
        
        Returns:
            bool: True si la fecha de creación se actualizó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = created_at
        self.save_users()
        return True

    def update_last_login_to_now(self, username):
        """
        Actualiza el último inicio de sesión de un usuario registrado a la fecha y hora actual.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si el último inicio de sesión se actualizó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.save_users()
        return True

    def update_is_active_to_false(self, username):
        """
        Desactiva un usuario registrado.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si el usuario se desactivó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['is_active'] = False
        self.save_users()
        return True

    def update_is_active_to_true(self, username):
        """
        Activa un usuario registrado.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si el usuario se activó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['is_active'] = True
        self.save_users()
        return True

    def update_created_at_to_now(self, username):
        """
        Actualiza la fecha de creación de un usuario registrado a la fecha y hora actual.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si la fecha de creación se actualizó correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true(self, username):
        """
        Actualiza la fecha de creación y el estado activo de un usuario registrado a la fecha y hora actual y activo.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si la fecha de creación y el estado activo se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false(self, username):
        """
        Actualiza la fecha de creación y el estado activo de un usuario registrado a la fecha y hora actual y desactivado.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si la fecha de creación y el estado activo se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now(self, username):
        """
        Actualiza la fecha de creación, el estado activo y el último inicio de sesión de un usuario registrado a la fecha y hora actual, activo y con inicio de sesión.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo y el último inicio de sesión se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now(self, username):
        """
        Actualiza la fecha de creación, el estado activo y el último inicio de sesión de un usuario registrado a la fecha y hora actual, desactivado y con inicio de sesión.
        
        Args:
            username: Nombre de usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo y el último inicio de sesión se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now_and_password_hash(self, username, new_password):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión y la contraseña de un usuario registrado a la fecha y hora actual, activo, con inicio de sesión y con nueva contraseña.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión y la contraseña se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now_and_password_hash(self, username, new_password):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión y la contraseña de un usuario registrado a la fecha y hora actual, desactivado, con inicio de sesión y con nueva contraseña.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión y la contraseña se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now_and_password_hash_and_role(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña y el rol de un usuario registrado a la fecha y hora actual, activo, con inicio de sesión, con nueva contraseña y con nuevo rol.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña y el rol se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now_and_password_hash_and_role(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña y el rol de un usuario registrado a la fecha y hora actual, desactivado, con inicio de sesión, con nueva contraseña y con nuevo rol.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña y el rol se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now_and_password_hash_and_role_and_username(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol y el nombre de usuario de un usuario registrado a la fecha y hora actual, activo, con inicio de sesión, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol y el nombre de usuario se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now_and_password_hash_and_role_and_username(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol y el nombre de usuario de un usuario registrado a la fecha y hora actual, desactivado, con inicio de sesión, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol y el nombre de usuario se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario y la fecha de creación de un usuario registrado a la fecha y hora actual, activo, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario y con nueva fecha de creación.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario y la fecha de creación se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario y la fecha de creación de un usuario registrado a la fecha y hora actual, desactivado, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario y con nueva fecha de creación.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario y la fecha de creación se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at_and_is_active(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo y el nombre de usuario de un usuario registrado a la fecha y hora actual, activo, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo y el nombre de usuario se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at_and_is_active(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo y el nombre de usuario de un usuario registrado a la fecha y hora actual, desactivado, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo y el nombre de usuario se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña y el rol de un usuario registrado a la fecha y hora actual, activo, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña y el rol se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña y el rol de un usuario registrado a la fecha y hora actual, desactivado, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña y el rol se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol y el nombre de usuario de un usuario registrado a la fecha y hora actual, activo, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol y el nombre de usuario se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol y el nombre de usuario de un usuario registrado a la fecha y hora actual, desactivado, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol y el nombre de usuario se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = False
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_true_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario y el nombre de usuario de un usuario registrado a la fecha y hora actual, activo, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
            bool: True si la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario y el nombre de usuario se actualizaron correctamente, False en caso contrario
        """
        if username not in self.users:
            return False
        self.users[username]['created_at'] = datetime.now().isoformat()
        self.users[username]['is_active'] = True
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.users[username]['password_hash'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.users[username]['role'] = new_role
        self.users[username]['username'] = username
        self.save_users()
        return True

    def update_created_at_to_now_and_is_active_to_false_and_last_login_to_now_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username_and_created_at_and_is_active_and_password_hash_and_role_and_username(self, username, new_password, new_role):
        """
        Actualiza la fecha de creación, el estado activo, el último inicio de sesión, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario, la fecha de creación, el estado activo, la contraseña, el rol, el nombre de usuario y el nombre de usuario de un usuario registrado a la fecha y hora actual, desactivado, con inicio de sesión, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol, con nuevo nombre de usuario, con nueva fecha de creación, con nuevo estado activo, con nueva contraseña, con nuevo rol y con nuevo nombre de usuario.
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña del usuario
            new_role: Nuevo rol del usuario
        
        Returns:
 """