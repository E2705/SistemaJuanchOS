#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class ProcessState(Enum):
    """Estados posibles de un proceso."""
    NEW = "new"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    TERMINATED = "terminated"

class Process:
    """Clase que representa un proceso en el sistema."""
    def __init__(self, pid: int, name: str):
        self.pid = pid
        self.name = name
        self.state = ProcessState.NEW
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.ended_at: Optional[datetime] = None

    def start(self):
        """Inicia el proceso."""
        self.state = ProcessState.RUNNING
        self.started_at = datetime.now()

    def terminate(self):
        """Termina el proceso."""
        self.state = ProcessState.TERMINATED
        self.ended_at = datetime.now()

    def __str__(self) -> str:
        return f"Process(pid={self.pid}, name='{self.name}', state={self.state.value})"

class ProcessManager:
    """Gestor de procesos del sistema."""
    def __init__(self):
        self.processes: Dict[int, Process] = {}
        self.next_pid = 1
        self.running_process: Optional[int] = None

    def create_process(self, name: str) -> int:
        """Crea un nuevo proceso."""
        pid = self.next_pid
        self.next_pid += 1

        process = Process(pid, name)
        self.processes[pid] = process
        process.state = ProcessState.READY

        return pid

    def terminate_process(self, pid: int) -> bool:
        """Termina un proceso."""
        if pid not in self.processes:
            return False

        process = self.processes[pid]
        process.terminate()
        del self.processes[pid]

        if self.running_process == pid:
            self.running_process = None

        return True

    def get_process_info(self, pid: int) -> Optional[Dict]:
        """Obtiene información de un proceso."""
        if pid not in self.processes:
            return None

        process = self.processes[pid]
        return {
            'pid': process.pid,
            'name': process.name,
            'state': process.state.value,
            'created_at': process.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'started_at': process.started_at.strftime("%Y-%m-%d %H:%M:%S") if process.started_at else None,
            'ended_at': process.ended_at.strftime("%Y-%m-%d %H:%M:%S") if process.ended_at else None
        }

    def list_processes(self) -> List[Dict]:
        """Lista todos los procesos en el sistema."""
        return [self.get_process_info(pid) for pid in self.processes.keys()]

    def get_running_process(self) -> Optional[Dict]:
        """Obtiene información del proceso en ejecución."""
        if self.running_process is None:
            return None
        return self.get_process_info(self.running_process) 