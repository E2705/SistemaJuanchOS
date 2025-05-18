#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Gestor de Memoria del Sistema Operativo
=============================================

Este módulo implementa el gestor de memoria del sistema operativo,
incluyendo:
- Asignación de memoria
- Liberación de memoria
- Fragmentación de memoria
- Paginación de memoria

Clases:
--------
- MemoryManager: Gestor principal de memoria
- MemoryBlock: Clase para representar bloques de memoria
"""

class MemoryBlock:
    """
    Representa un bloque de memoria en el sistema.
    
    Atributos:
        start_address: Dirección de inicio
        size: Tamaño del bloque
        is_allocated: Indica si el bloque está asignado
        process_id: ID del proceso que usa el bloque
        next_block: Referencia al siguiente bloque
    
    Métodos:
        split: Divide el bloque en dos
        merge: Fusiona con el siguiente bloque
        get_info: Obtiene información del bloque
    """
    
    def __init__(self, start_address, size):
        self.start_address = start_address
        self.size = size
        self.is_allocated = False
        self.process_id = None
        self.next_block = None

class MemoryManager:
    """
    Implementa el gestor de memoria del sistema operativo.
    
    Atributos:
        total_memory: Memoria total disponible
        memory_blocks: Lista de bloques de memoria
        allocated_memory: Memoria asignada
        free_memory: Memoria libre
    
    Métodos:
        allocate: Asigna memoria a un proceso
        deallocate: Libera memoria de un proceso
        get_memory_info: Obtiene información de la memoria
        defragment: Desfragmenta la memoria
        find_free_block: Busca un bloque libre
    """
    
    def __init__(self, total_memory=1024):
        self.total_memory = total_memory
        self.memory_blocks = [MemoryBlock(0, total_memory)]
        self.allocated_memory = 0
        self.free_memory = total_memory

