
from __future__ import division
from numpy import pi
import numpy as np
import matplotlib.pyplot as plt

class BipolarCircuit():
    def __add__(self, other):
        return Serial(self, other)
    def __or__(self, other):
        return Parallel(self, other)


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
my_circuit1 = Resistor(1000) + Capacitor(1E-5)
print(my_circuit.impedance(5000))

Tfreq = np.logspace(3, 7)
plt.semilogx(Tfreq, np.abs(my_circuit1.impedance(Tfreq)))
plt.show()