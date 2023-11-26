# Press Shift+F10 to execute it or replace it with your code.
# OOP consepts in python Code
# Classes, Functions in side Classes, Inheritance, Ecapsulation and properties (getter and setter)


class Patient:
    def __init__(self, name, age):
        self.name=name
        self.age=age

    def __str__(self):
        return f'{self.name} {self.age} years'
class HeartPatient(Patient):
    def __init__(self,name,age, disease):
        super().__init__(name,age)
        self.disease=disease
        self.__costs =None
        self._num_of_visits=0

    def __str__(self):
        return f'{self.name} {self.age} years {self.disease} patients'
    @property
    def Costs(self):
        return self.__costs

    @Costs.setter
    def Costs(self, value):
        self.__costs= self._calc_cost(value)

    def code(self):
        self._num_of_visits+=1
    def _calc_cost(self, base_value):
        if self._num_of_visits <10:
            return base_value
        if self._num_of_visits<100:
            return base_value*2
        return  base_value*3

hp= HeartPatient('Nor','45','Heart')

for i in range(70):
    hp.code()

print(hp)
hp.Costs=30000
print(hp.Costs)
