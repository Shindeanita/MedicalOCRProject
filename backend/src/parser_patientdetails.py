import re
from backend.src.parser_generic import MedicalDocParser

class PatientDetailsParser(MedicalDocParser):
    def __init__(self,text):
        MedicalDocParser.__init__(self,text)


    def parse(self):
        return {
            'patientname' : self.get_patient_name(),
            'phonenumber' : self.get_patient_number(),
            'hepBvaccination' : self.get_vaccination(),
            'medical_problem' : self.get_medicalproblem()
        }


    def get_patient_name(self):
        pattern = 'Patient Information(.*?)\(\d{3}\)'
        matchs = re.findall(pattern, self.text,re.DOTALL)
        if len(matchs) > 0:
            name = self.remove_noise_from_text(matchs)
            return name.strip()

    def remove_noise_from_text(self,text):
        name = text[0].replace('Birth Date', '')
        text=name.strip()
        pattern = '((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[ \d]+)'
        matches = re.findall(pattern, text)
        date = matches[0][0]
        name = name.replace(date, " ").strip()
        return name

    def get_patient_number(self):
        pattern = 'Patient Information.*?(\(\d{3}\) \d{3}-\d{4})'
        match = re.findall(pattern, self.text, re.DOTALL)
        if len(match) > 0 :
            return match[0].strip()

    def get_vaccination(self):
        pattern = 'Have you had the Hepatitis B vaccination\?.*(Yes|No)'
        match = re.findall(pattern, self.text, flags=re.DOTALL)
        if len(match)>0:
            return match[0].strip()

    def get_medicalproblem(self):
        pattern = 'List any Medical Problems .*?\:(.*)'
        match = re.findall(pattern, self.text, flags=re.DOTALL)
        if len(match) > 0:
            return match[0].strip()

if __name__ == '__main__':
    doc_text = '''17/12/2020
    Patient Medical Record
    Patient Information Birth Date
    Kathy Crawford May 6 1972
    (737) 988-0851 Weight’
    9264 Ash Dr 95
    New York City, 10005 '
    United States Height:
    190
    In Case of Emergency
    ee J
    Simeone Crawford 9266 Ash Dr
    New York City, New York, 10005
    Home phone United States
    (990) 375-4621
    Work phone
    Genera! Medical History
    nn ee
    Chicken Pox (Varicella): Measies:
    IMMUNE
    IMMUNE
    Have you had the Hepatitis B vaccination?
    No
    List any Medical Problems (asthma, seizures, headaches):
    Migraine'''

    doc_text2='''Patient Medical Record

    Patient Information Birth Date

    Jerry Lucas May 2 1998

    (279) 920-8204 Weight:

    4218 Wheeler Ridge Dr 57

    Buffalo, New York, 14201 Height:

    United States gnt
    170

    In Case of Emergency

    - eee

    Joe Lucas . 4218 Wheeler Ridge Dr
    Buffalo, New York, 14201
    Home phone United States
    Work phone

    General Medical History

    Chicken Pox (Varicelia): Measles: ..

    IMMUNE NOT IMMUNE

    Have you had the Hepatitis B vaccination?

    Yes

    | List any Medical Problems (asthma, seizures, headaches):
    N/A '''
    pp2 = PatientDetailsParser(doc_text2)
    pp = PatientDetailsParser(doc_text)

    print(pp.parse())
    print(pp2.parse())