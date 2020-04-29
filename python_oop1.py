#
# class MyClass():
#     i = 12345
#
#     def f(self):
#         return ("hello world")
#
#
# x = MyClass.i
# y = MyClass()
#
# print(dir(MyClass))
# print(dir(x))
# print(dir(y))
#
# print(x)
# print(y.f())
#

# class MyClass():
#     def __init__(self):
#         self.data = []
#
#     def f(self):
#         return "hello world"
#
#
#
# x = MyClass()
# x.counter = 1
# while (x.counter < 10):
#     x.counter = 2 * x.counter
# print(x.counter)
# del x.counter





#
# class my_car():
#     def __init__(self, color, milage):
#         self.color = color
#         self.milage = milage
#
# c1 = my_car("red", 4000)
# print(c1.color)
# print(c1.milage)
# print(dir(c1))
# print(dir(my_car))


# class Complex():
#     def __init__(self, realpart, imagpart):
#         self.realpart = realpart
#         self.imagpart = imagpart
#
#     def Show(self):
#         return (self.realpart,self.imagpart)
#
# z1 = Complex(1,2)
# print(z1.realpart,z1.imagpart)
# print(z1.Show())

from __future__ import division
from numpy import pi
import numpy as np
import matplotlib.pyplot as plt


class BipolarCircuit():
    def __add__(self,other):
        return Serial(self,other)
    def __or__(self, other):
        return Parallel(self,other)


class Combination(BipolarCircuit):
    def __init__(self, *list_of_circuit):
        self.list_of_circuit = list_of_circuit
        self.simplify()


    def __repr__(self):
        args = ', '.join([repr(item) for item in self.list_of_circuit])
        return '{self.__class__.__name__}({args})'.format(self=self, args=args)

    def simplify(self):
        new_list = []
        for elm in self.list_of_circuit:
            if isinstance(elm, self.__class__):
                new_list.extend(elm.list_of_circuit)
            else:
                new_list.append(elm)
        self.list_of_circuit = new_list

class Serial(Combination):
    def impedance(self, frequency):
        return sum([elm.impedance(frequency) for elm in self.list_of_circuit])

    # def impedance(self, frequency):
    #     result = 0
    #     for elm in self.list_of_circuit:
    #         result += elm.impedance(frequency)
    #     return result


class Parallel(Combination):
    def impedance(self, frequency):
        return 1/(sum([1/elm.impedance(frequency) for elm in self.list_of_circuit]))



##############  Definition of the devices (resistor, capacitor and inductor) #######33
class Device(BipolarCircuit):
    def __init__(self,value):
        self.value = value

class Resistor(Device):
    def impedance(self,frequency):
        return self.value

class Capacitor(Device):
    def impedance(self, frequency):
        omega = 2 * pi * frequency
        return 1/(1j*omega * self.value)

class Inductor(Device):
    def impedance(self, frequency):
        omega = 2 * pi * frequency
        return (1j * omega * self.value)
######################################################################################
# r1 = Resistor(50)
# print(r1.impedance(10))
# c1 = Capacitor(1E-6)
# print(c1.impedance(50))

my_circuit = (Resistor(10) | Capacitor(1E-5) | Inductor(10E-6)) + Resistor(5)
print(my_circuit.impedance(5000))

Tfreq = np.logspace(3, 7)
plt.semilogx(Tfreq, np.abs(my_circuit.impedance(Tfreq)))
plt.show()