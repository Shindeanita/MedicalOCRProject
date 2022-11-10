from backend.src.parser_patientdetails import PatientDetailsParser
import pytest

@pytest.fixture()
def doc_empty():
    return PatientDetailsParser('')

@pytest.fixture()
def doc_text_kathy():
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
    return PatientDetailsParser(doc_text)

@pytest.fixture()
def doc_text_jerry():
    doc_text= '''Patient Medical Record
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
    List any Medical Problems (asthma, seizures, headaches):
    N/A'''
    return PatientDetailsParser(doc_text)

def test_get_name(doc_empty,doc_text_kathy,doc_text_jerry):
    assert doc_empty.get_patient_name() == None
    assert doc_text_kathy.get_patient_name() == 'Kathy Crawford'
    assert doc_text_jerry.get_patient_name() == 'Jerry Lucas'

def test_get_phone(doc_empty,doc_text_kathy,doc_text_jerry):
    assert doc_empty.get_patient_number() == None
    assert doc_text_kathy.get_patient_number() == '(737) 988-0851'
    assert doc_text_jerry.get_patient_number() == '(279) 920-8204'

def test_get_hbvaccination(doc_empty,doc_text_kathy,doc_text_jerry):
    assert doc_empty.get_vaccination() == None
    assert doc_text_kathy.get_vaccination() =='No'
    assert doc_text_jerry.get_vaccination() =='Yes'

def test_get_medicalproblem(doc_empty,doc_text_kathy,doc_text_jerry):
    assert doc_empty.get_medicalproblem() == None
    assert doc_text_kathy.get_medicalproblem() == 'Migraine'
    assert doc_text_jerry.get_medicalproblem() == 'N/A'

def test_parse(doc_empty,doc_text_kathy,doc_text_jerry):
    record_empty = doc_empty.parse()
    record_empty == {
        'patientname': None,
        'phonenumber': None,
        'hepBvaccination': None,
        'medical_problem': None

    }
    record_kathy = doc_text_kathy.parse()
    record_kathy == {
        'patientname': 'Kathy Crawford',
        'phonenumber': '(737) 988-0851',
        'hepBvaccination': 'No',
        'medical_problem': 'Migraine'
    }
    record_jerry = doc_text_jerry.parse()
    record_jerry == {
        'patientname': 'Jerry Lucas',
        'phonenumber': '(279) 920-8204',
        'hepBvaccination': 'Yes',
        'medical_problem': 'N/A'
    }

