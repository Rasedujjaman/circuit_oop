
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
# L = 4
# x = np.linspace(0,10, 500, endpoint= False)
#
# n = []  # define a blank array
# for i in range(1000):
#     nf = 2*i + 1
#     n.append(nf)
# #print(n)
#
# fx = []
# fsum = 0*x
# coef = []
# for p in n:
#     temp = (4/np.pi)*(1/float(p))*np.sin(p*np.pi*x/L)
#     fsum = np.add(fsum,temp)
#     fx.append(temp)
#
#
# plt.plot(x, fsum)
#




my_circuit = (Resistor(10) | Capacitor(1E-5) | Inductor(10E-6)) + Resistor(5)
my_circuit1 = Resistor(1000) + Capacitor(1E-5)
print(my_circuit1.impedance(50))

aa = [1.2732395447351628, 0.4244131815783876, 0.25464790894703254, 0.18189136353359467, 0.14147106052612918, 0.11574904952137843, 0.09794150344116637, 0.08488263631567752, 0.07489644380795075, 0.06701260761764014, 0.06063045451119822, 0.05535824107544186, 0.050929581789406514, 0.047157020175376395, 0.043904811887419404, 0.041072243378553634, 0.038583016507126144, 0.03637827270671894, 0.034411879587436835, 0.03264716781372212]
frq = [0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75, 8.25, 8.75, 9.25, 9.75]
aa_array = np.array(aa)
frq_array = np.array(frq)
print (aa_array)

Tfreq = np.logspace(3, 7)
y = np.abs(my_circuit1.impedance(frq_array))
y = y*aa_array
plt.semilogx(frq_array, y)
plt.show()
###########################################################################








# Tfreq = np.logspace(3, 7)
# plt.semilogx(Tfreq, np.abs(my_circuit1.impedance(Tfreq)))
# plt.show()