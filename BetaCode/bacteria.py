import random
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Type, Tuple

class Gen(ABC):
    
    def __init__(self, value:float, max_value:float, min_value:float, shance:float=0.5, coef:float=0.05):
        """присвоение значения"""
        self.value = value
        self.max_value = max_value
        self.min_value = min_value
        self.shance = shance
        self.coef = coef
        
    def copy(self) -> "Gen":
        value = self.value
        if random.random() <= self.shance:
            value += np.random.normal(0, self.coef)
            value = np.clip(value, self.min_value, self.max_value) # Принудительное максимальное значение
            value = round(value, 2)
        return self.__class__(value)

class SizeGen(Gen):
        def __init__(self, value:float=1, max_value:float=20, min_value:float=0.1):
            super().__init__(value, max_value, min_value)

class SpeedGen(Gen):
        def __init__(self, value:float=1, max_value:float=50, min_value:float=0.1):
            super().__init__(value, max_value, min_value)

class ColordGen(Gen):
        def __init__(self, value:str="red", shance:float=0):
            super().__init__(value,0,0, shance=shance)
        
class ChildrendGen(Gen):
        def __init__(self, value:float=1, max_value:float=10, min_value:float=1, shance:float=0.1, coef:float = 0.1):
            super().__init__(value, max_value, min_value, shance, coef)
            
class BatledGen(Gen):
        def __init__(self, value:float=1, max_value:float=10, min_value:float=0.5, shance:float=0.5, coef:float = 0.1):
            super().__init__(value, max_value, min_value, shance, coef)    
            
class GrowthSpeedGen(Gen):
        def __init__(self, value:float=1, max_value:float=10, min_value:float=1, shance:float=0.5, coef:float = 0.1):
            super().__init__(value, max_value, min_value, shance, coef)

class DNAConstructor():
    
    def __init__(self, mask:Dict[str,Gen]):
        self.mask = mask
        
    def create(self, standart={}):
        gens = {}
        for gen_name, gen_cls in self.mask.items():
            gens[gen_name] = gen_cls()
        gens.update(standart)
        return DNA(gens, self)
    
    def copy(self, dna:Dict[str,Gen]):
        gens = {name:gen.copy() for name, gen in dna.gens.items()} 
        return DNA(gens, self)      

class DNA():
    
    def __init__(self, gens:Dict[str,Gen], constructor:DNAConstructor):
        self.constructor = constructor
        self.gens = gens
    
    def __str__(self):
        return "".join([f"{i}: {x.value}\n" for i, x in self.gens.items()])
    
    def copy(self):
        return self.constructor.copy(self)

class BacteriaBiology():
    pass

class BacteriaSprite():
    pass
    
class Bacteria():
    
    def __init__(self):
        self.biology = BacteriaBiology()
        self.sprite = BacteriaSprite()
        
    def update(self):
        pass
    
if __name__ == "__main__":
    mask = {"speed":SpeedGen, "size":SizeGen, "color":ColordGen, "children":ChildrendGen, "batle":BatledGen, "growth":GrowthSpeedGen}
    dna_create = DNAConstructor(mask)
    j = dna_create.create()
    for x in range(100000):
        j = j.copy()
        print(j)