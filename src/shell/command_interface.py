#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class CommandInterface:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.commands = {
            'help': self.help,
            'mkdir': self.create_directory,
            'cd': self.change_directory,
            'ls': self.list_directory,
            'touch': self.create_file,
            'cat': self.read_file,
            'echo': self.write_file,
            'rm': self.delete_file,
            'pwd': self.print_working_directory,
            'exit': self.exit
        }

    def execute_command(self, command_line):
        if not command_line.strip():
            return None

        # Verificar que los gestores del sistema estén disponibles
        if not self.user_manager or not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"

        parts = command_line.split()
        command = parts[0].lower()
        args = parts[1:]

        if command in self.commands:
            try:
                return self.commands[command](*args)
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return f"Comando no reconocido: {command}\nUse 'help' para ver los comandos disponibles"

    def help(self, *args):
        """Muestra la lista de comandos disponibles"""
        help_text = "Comandos disponibles:\n"
        for cmd, func in self.commands.items():
            help_text += f"- {cmd}: {func.__doc__}\n"
        return help_text

    def create_directory(self, name, *args):
        """Crea un nuevo directorio"""
        if not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"
        if self.user_manager.file_system.create_directory(name):
            return f"Directorio '{name}' creado"
        return f"No se pudo crear el directorio '{name}'"

    def change_directory(self, path, *args):
        """Cambia al directorio especificado"""
        if not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"
        if self.user_manager.file_system.change_directory(path):
            return f"Directorio actual: {self.user_manager.file_system.get_current_directory()}"
        return f"No se pudo cambiar al directorio '{path}'"

    def list_directory(self, *args):
        """Lista el contenido del directorio actual"""
        if not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"
        contents = self.user_manager.file_system.list_directory()
        if not contents:
            return "El directorio está vacío"
        return "\n".join(str(item) for item in contents)

    def create_file(self, name, *args):
        """Crea un nuevo archivo"""
        if not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"
        if self.user_manager.file_system.create_file(name):
            return f"Archivo '{name}' creado"
        return f"No se pudo crear el archivo '{name}'"

    def read_file(self, name, *args):
        """Muestra el contenido de un archivo"""
        if not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"
        content = self.user_manager.file_system.read_file(name)
        if content is not None:
            return content
        return f"No se pudo leer el archivo '{name}'"

    def write_file(self, name, *args):
        """Escribe contenido en un archivo"""
        if not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"
        content = " ".join(args)
        if self.user_manager.file_system.write_file(name, content):
            return f"Contenido escrito en '{name}'"
        return f"No se pudo escribir en el archivo '{name}'"

    def delete_file(self, name, *args):
        """Elimina un archivo"""
        if not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"
        if self.user_manager.file_system.delete_file(name):
            return f"Archivo '{name}' eliminado"
        return f"No se pudo eliminar el archivo '{name}'"

    def print_working_directory(self, *args):
        """Muestra el directorio de trabajo actual"""
        if not self.user_manager.file_system:
            return "Error: Sistema de archivos no disponible"
        return self.user_manager.file_system.get_current_directory()

    def exit(self, *args):
        """Cierra la terminal"""
        return "exit"

    def cleanup(self):
        """Limpia los recursos antes de cerrar"""
        pass 