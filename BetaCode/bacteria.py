import random
from abc import ABC, abstractmethod

class Gen(ABC):
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def __add__(self, other):
        pass
    
class Bacteria(ABC):
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def __add__(self, other):
        pass