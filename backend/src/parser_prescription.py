import re

from backend.src.parser_generic import MedicalDocParser


class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self, text)


    def get_field(self, field_name):
        pattern_dict = {
            'patient_name': {'pattern': 'Name:(.*)Date', 'flags': 0},
            'address': {'pattern': 'Address:(.*)\n', 'flags': 0},
            'medicine': {'pattern': 'Address:[^\n]*(.*)Directions', 'flags': re.DOTALL},
            'direction': {'pattern': 'Directions:(.*)Refill', 'flags': re.DOTALL},
            'refill': {'pattern': 'Refill:(.\d*)', 'flags': 0}
        }
        pattern_object = pattern_dict.get(field_name)
        if pattern_object:
            matchs = re.findall(pattern_object['pattern'], self.text, flags=pattern_object['flags'])
            if len(matchs) > 0:
                return matchs[0].strip()

    def parse(self):
        return {
            'patient_name': self.get_field('patient_name'),
            'address': self.get_field('address'),
            'medicine': self.get_field('medicine'),
            'direction': self.get_field('direction'),
            'refill': self.get_field('refill')
        }

    # def get_name(self):
    #     pattern = 'Name:(.*)Date'
    #     matchs = re.findall(pattern,self.text)
    #     if len(matchs) > 0:
    #         return matchs[0].strip()
    #
    # def get_address(self):
    #     pattern = 'Address:(.*)\n'
    #     matchs = re.findall(pattern,self.text)
    #     if len(matchs) > 0:
    #         return matchs[0].strip()
    #
    # def get_medicine(self):
    #     pattern = 'Address:[^\n]*(.*)Directions'
    #     matchs = re.findall(pattern,self.text,flags=re.DOTALL)
    #     if len(matchs) > 0:
    #         return matchs[0].strip()
    #
    # def get_directions(self):
    #     pattern = 'Directions:(.*)Refill'
    #     matchs = re.findall(pattern, self.text, flags=re.DOTALL)
    #     if len(matchs) > 0:
    #         return matchs[0].strip()
    #
    # def get_refill(self):
    #     pattern = 'Refill:(.\d*)'
    #     matchs = re.findall(pattern, self.text)
    #     if len(matchs) > 0:
    #         return matchs[0].strip()


if __name__ == '__main__':
    doc_text = '''Dr John Smith, M.D
    2 Non-Important Street,
    New York, Phone (000)-111-2222
    Name: Marta Sharapova Date: 5/11/2022
    Address: 9 tennis court, new Russia, DC
    
    Prednisone 20 mg
    Lialda 2.4 gram
    Directions:
    Prednisone, Taper 5 mg every 3 days,
    Finish in 2.5 weeks a
    Lialda - take 2 pill everyday for 1 month

    Refill: 2 times'''
    pp = PrescriptionParser(doc_text)

    print(pp.parse())
