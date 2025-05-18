#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MemoryBlock:
    """Bloque de memoria."""
    start: int
    size: int
    is_free: bool
    process_id: Optional[int] = None
    allocated_at: Optional[datetime] = None

class MemoryManager:
    """Gestor de memoria del sistema."""
    def __init__(self, total_memory: int = 1024):
        """
        Inicializa el gestor de memoria.
        
        Args:
            total_memory: Tamaño total de la memoria en MB.
        """
        self.total_memory = total_memory
        self.used_memory = 0
        self.memory_blocks: list[MemoryBlock] = [
            MemoryBlock(0, total_memory, True)
        ]
        self.process_memory: Dict[int, list[MemoryBlock]] = {}

    def allocate_memory(self, process_id: int, size: int) -> Optional[int]:
        """
        Asigna memoria a un proceso.
        
        Args:
            process_id: ID del proceso.
            size: Tamaño de memoria a asignar en MB.
            
        Returns:
            Dirección de inicio de la memoria asignada o None si no hay espacio.
        """
        if size <= 0 or size > self.total_memory:
            return None

        # Buscar el mejor bloque libre (Best Fit)
        best_block = None
        best_block_index = -1
        min_waste = float('inf')

        for i, block in enumerate(self.memory_blocks):
            if block.is_free and block.size >= size:
                waste = block.size - size
                if waste < min_waste:
                    min_waste = waste
                    best_block = block
                    best_block_index = i

        if best_block is None:
            return None

        # Dividir el bloque si es necesario
        if best_block.size > size:
            new_block = MemoryBlock(
                best_block.start + size,
                best_block.size - size,
                True
            )
            self.memory_blocks.insert(best_block_index + 1, new_block)
            best_block.size = size

        # Asignar el bloque
        best_block.is_free = False
        best_block.process_id = process_id
        best_block.allocated_at = datetime.now()
        self.used_memory += size

        # Registrar el bloque en el proceso
        if process_id not in self.process_memory:
            self.process_memory[process_id] = []
        self.process_memory[process_id].append(best_block)

        return best_block.start

    def deallocate_memory(self, process_id: int) -> bool:
        """
        Libera la memoria asignada a un proceso.
        
        Args:
            process_id: ID del proceso.
            
        Returns:
            True si se liberó la memoria correctamente, False en caso contrario.
        """
        if process_id not in self.process_memory:
            return False

        # Liberar todos los bloques del proceso
        for block in self.process_memory[process_id]:
            block.is_free = True
            block.process_id = None
            block.allocated_at = None
            self.used_memory -= block.size

        # Eliminar el proceso del registro
        del self.process_memory[process_id]

        # Compactar bloques libres adyacentes
        self._compact_free_blocks()
        return True

    def get_memory_usage(self) -> Dict:
        """
        Obtiene estadísticas de uso de memoria.
        
        Returns:
            Diccionario con estadísticas de memoria.
        """
        total_free = sum(block.size for block in self.memory_blocks if block.is_free)
        
        return {
            'total_memory': self.total_memory,
            'used_memory': self.used_memory,
            'free_memory': total_free,
            'total_blocks': len(self.memory_blocks),
            'free_blocks': len([b for b in self.memory_blocks if b.is_free]),
            'allocated_blocks': len([b for b in self.memory_blocks if not b.is_free])
        }

    def _compact_free_blocks(self):
        """Compacta bloques libres adyacentes."""
        i = 0
        while i < len(self.memory_blocks) - 1:
            current = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]
            
            if current.is_free and next_block.is_free:
                # Combinar bloques adyacentes libres
                current.size += next_block.size
                self.memory_blocks.pop(i + 1)
            else:
                i += 1 