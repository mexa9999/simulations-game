import random
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Type, Tuple
from bitarray import bitarray
from copy import deepcopy
from functools import cached_property




class SubGen:
    
    random_segmen_mutate = [bitarray(bin(x)[2:].zfill(3)) for x in range(8)]
    
    def __init__(self, size, coef=0.1, bit = None):
        self.bitaray = bitarray(bin(random.getrandbits(size))[2:].zfill(size)) if bit is None else bit
        self.size = size
        self.coef = coef
        
        
    def bit_mutate(self, data):
        index = random.randrange(self.size)
        data[index] = not data[index]
        return data

    def segment_mutate(self, data):
        h = random.randrange(self.size - 2)
        data[h:h + 3] = random.choice(SubGen.random_segmen_mutate)
        return data

    def segment_invert(self, data):
        h =random.randrange(self.size - 2)
        df = data[h:h + 3]
        df.invert()
        data[h:h + 3] = df
        return data
    
    def reproduct(self):
        data = self.bitaray.copy()
        if random.random() <= 0.5:
            data = self.bit_mutate(data)
        if random.random() <= 0.25:
            data = self.segment_invert(data)
        if random.random() <= 0.1:
            data = self.segment_mutate(data)
        return SubGen(self.size, self.coef, data)
    
    @cached_property
    def value(self):
        return sum(self.bitaray)*self.coef

class Gen(ABC):
    
    def __init__(self, strong_subgene, medium_subgene, weak_subgene):
        """присвоение значения"""
        self.strong_subgene = strong_subgene
        self.medium_subgene = medium_subgene
        self.weak_subgene = weak_subgene
        
    def reproduct(self):
        strong_subgene = self.strong_subgene.reproduct()
        medium_subgene  = self.medium_subgene.reproduct()
        weak_subgene   = self.weak_subgene.reproduct()
        return self.__class__(strong_subgene,medium_subgene,weak_subgene)
    
    @cached_property
    def value(self):
        return self.strong_subgene.value+self.medium_subgene.value+self.weak_subgene.value


class SizeGen(Gen):
    pass

class SpeedGen(Gen):
    pass

class ColordGen(Gen):
    pass
        
class ChildrendGen(Gen):
    pass
            
class BatledGen(Gen):
    pass 
            
class GrowthSpeedGen(Gen):
    pass

class DNAConstructor():
    
    def __init__(self, mask:Dict[str,Gen]):
        self.mask = mask
        
    def create(self, sub_size, standart={}):
        gens = {gen_name: gen_cls(SubGen(sub_size,1),SubGen(sub_size,0.5),SubGen(sub_size,0.25)) for gen_name, gen_cls in self.mask.items()}
        gens.update(standart)

        return DNA(gens, self)
    
    def copy(self, dna:Dict[str,Gen]):
        gens = {name: gen.reproduct() for name, gen in dna.gens.items()}
        return DNA(gens, self)      

class DNA():
    
    def __init__(self, gens:Dict[str,Gen], constructor:DNAConstructor):
        self.constructor = constructor
        self.gens = gens
    
    def __str__(self):
        return "\n".join([f"{name}: {gen.value}" for name, gen in self.gens.items()])
    
    def copy(self):
        return self.constructor.copy(self)
    
    def summ(self):
        return sum(gen.value for gen in self.gens.values())

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
    mask = {"size":SizeGen, "speed":SpeedGen, "color":ColordGen, "children":ChildrendGen, "batle":BatledGen, "growth":GrowthSpeedGen}
    dna_create = DNAConstructor(mask)
    j = dna_create.create(50)
    makh = 0
    for x in range(10000000):
        j = j.copy()
        if j.summ()>makh:
            makh = j.summ()
            print(makh, j)