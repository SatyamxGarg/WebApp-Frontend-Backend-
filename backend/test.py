# class method
class Test:
    name = 'ABC'
    @classmethod
    def func(cls):
        cls.name = 'XYZ'
print(Test.name)
obj=Test()
print(obj,"object==")
obj.func()
print(Test.name,"after==")
        
        
class mathOper:
    pi=3.14159
    @classmethod
    def circle(cls,radi):
        print(cls.pi*radi*radi)
    
    @staticmethod
    def func(x,y):
        return x+y        
    
mathOper.circle(5)
print(mathOper.func(5,5))

#abstract class and method

from abc import ABC, abstractmethod
class Test1(ABC):
    @abstractmethod
    def sound(self):
        pass
    @abstractmethod
    def legs(self):
        pass
    def func(self):
        return "Normal function"

class Dog(Test1):
    def sound(self):
        return "bark"
    
    def legs(self):
        return "4 legs"

d=Dog()
print(d.sound())
print(d.legs())
print(d.func())


# data classes

from dataclasses import dataclass
@dataclass
class Person:
    name: str
    age: int
    
oj=Person(name="ABC",age=23)
oj2=Person(name="ABC",age=24)
print(oj==oj2)
print(oj2)


#asyncio

import asyncio
async def fn():
	task=asyncio.create_task(fn2())
	print("one")
	#await asyncio.sleep(1)
	#await fn2()
	print('four')
	await asyncio.sleep(10)
	print('five')
	await asyncio.sleep(1)

async def fn2():
	#await asyncio.sleep(1)
	print("two")
	await asyncio.sleep(1)
	print("three")
	
asyncio.run(fn())