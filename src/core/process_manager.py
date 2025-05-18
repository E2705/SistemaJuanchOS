#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Gestor de Procesos del Sistema Operativo
===============================================

Este módulo implementa el gestor de procesos del sistema operativo,
incluyendo:
- Creación y eliminación de procesos
- Planificación de procesos
- Estados de procesos
- Comunicación entre procesos

Clases:
--------
- ProcessManager: Gestor principal de procesos
- Process: Clase para representar procesos
"""

from datetime import datetime
import threading
import time

class Process:
    """
    Representa un proceso en el sistema operativo.
    
    Atributos:
        pid: Identificador del proceso
        name: Nombre del proceso
        state: Estado del proceso (running, ready, blocked)
        priority: Prioridad del proceso
        created_at: Fecha de creación
        cpu_time: Tiempo de CPU utilizado
        memory_usage: Uso de memoria
    
    Métodos:
        start: Inicia el proceso
        stop: Detiene el proceso
        pause: Pausa el proceso
        resume: Reanuda el proceso
        get_info: Obtiene información del proceso
    """
    
    def __init__(self, pid, name, priority=1):
        self.pid = pid
        self.name = name
        self.state = "ready"
        self.priority = priority
        self.created_at = datetime.now()
        self.cpu_time = 0
        self.memory_usage = 0
        self.thread = None

class ProcessManager:
    """
    Implementa el gestor de procesos del sistema operativo.
    
    Atributos:
        processes: Diccionario de procesos activos
        next_pid: Siguiente PID disponible
        running_process: Proceso actual en ejecución
        process_lock: Lock para sincronización
    
    Métodos:
        create_process: Crea un nuevo proceso
        terminate_process: Termina un proceso
        list_processes: Lista los procesos activos
        get_process_info: Obtiene información de un proceso
        schedule: Planifica los procesos
        update_process_state: Actualiza el estado de un proceso
    """
    
    def __init__(self):
        self.processes = {}
        self.next_pid = 1
        self.running_process = None
        self.process_lock = threading.Lock()

