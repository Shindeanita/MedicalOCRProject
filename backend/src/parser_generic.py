import abc
#parent class use the abstract method
class MedicalDocParser(metaclass=abc.ABCMeta):
    def __init__(self,text):
        self.text = text

    @abc.abstractmethod
    def parse(self):
        pass

