# domain/models.py
from dataclasses import dataclass
from typing import List

@dataclass
class CPU:
    model: str
    cores: int
    threads: int
    frequency: float

@dataclass
class Memory:
    total: int
    available: int

@dataclass
class Disk:
    total: int
    free: int

@dataclass
class GPU:
    name: str
    memory_total: int
    memory_free: int
    memory_used: int

@dataclass
class SystemInfo:
    cpu: CPU
    memory: Memory
    disk: Disk
    gpu: List[GPU]

@dataclass
class User:
    username: str
    password: str
