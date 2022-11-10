from backend.src.parser_prescription import PrescriptionParser
import pytest

@pytest.fixture()
def doc_maria_1():
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
    return PrescriptionParser(doc_text)

@pytest.fixture()
def doc_virat_1():
    doc_text = '''Dr John >mith, M.D
    2 Non-Important street,
    New York, Phone (900)-323- ~2222
    Name:  Virat Kohli Date: 2/05/2022
    Address: 2 cricket blvd, New Delhi
    | Omeprazole 40 mg
    Directions: Use two tablets daily for three months
    Refill: 3 times'''
    return PrescriptionParser(doc_text)

@pytest.fixture()
def doc_text_empty():
    return PrescriptionParser('')

def test_get_name(doc_maria_1,doc_virat_1,doc_text_empty):
    assert doc_maria_1.get_field('patient_name') == "Marta Sharapova"
    assert doc_virat_1.get_field('patient_name') == "Virat Kohli"
    assert doc_text_empty.get_field('patient_name') == None
   # assert doc_maria_1.get_field('patient_name') == "Adam Jhon"


def test_get_address(doc_maria_1,doc_virat_1,doc_text_empty):
    assert doc_maria_1.get_field('address') == "9 tennis court, new Russia, DC"
    assert doc_virat_1.get_field('address') == "2 cricket blvd, New Delhi"
    assert doc_text_empty.get_field('address') == None

def test_get_medicine(doc_text_empty,doc_virat_1,doc_maria_1):
    assert doc_maria_1.get_field('medicine') == '''Prednisone 20 mg
        Lialda 2.4 gram'''
    assert doc_virat_1.get_field('medicine') == '| Omeprazole 40 mg'
    assert doc_text_empty.get_field('medicine') == None


def test_get_direction(doc_maria_1,doc_virat_1,doc_text_empty):
    assert doc_maria_1.get_field('direction') == '''Prednisone, Taper 5 mg every 3 days,
        Finish in 2.5 weeks a
        Lialda - take 2 pill everyday for 1 month'''
    assert doc_virat_1.get_field('direction') == 'Use two tablets daily for three months'
    assert doc_text_empty.get_field('direction') == None

def test_get_refill(doc_text_empty,doc_virat_1,doc_maria_1):
    assert doc_maria_1.get_field('refill') == '2'
    assert doc_virat_1.get_field('refill') == '3'
    assert doc_text_empty.get_field('refill') == None

def test_parse(doc_text_empty,doc_virat_1,doc_maria_1):
    record_maria = doc_maria_1.parse()
    assert record_maria['patient_name'] == 'Marta Sharapova'
    assert record_maria['address'] == '9 tennis court, new Russia, DC'
    assert record_maria['medicine'] == '''Prednisone 20 mg
        Lialda 2.4 gram'''
    assert record_maria['direction'] == '''Prednisone, Taper 5 mg every 3 days,
        Finish in 2.5 weeks a
        Lialda - take 2 pill everyday for 1 month'''
    assert record_maria['refill'] == '2'

    record_virat = doc_virat_1.parse()
    assert record_virat == {
        'patient_name' : 'Virat Kohli',
        'address' : '2 cricket blvd, New Delhi',
        'direction': 'Use two tablets daily for three months',
        'medicine' : '| Omeprazole 40 mg',
        'refill':'3'
    }

    record_empty = doc_text_empty.parse()
    assert record_empty == {
        'patient_name': None,
        'address':None,
        'direction': None,
        'medicine': None,
        'refill': None
    }

doc_text_1 = '''Dr John Smith, M.D
    2 Non-Important Street,
    New York, Phone (000)-111-2222
    Name: Adam Jhon Date: 5/11/2022
    Address: 9 tennis court, new Russia, DC

    Prednisone 20 mg
    Lialda 2.4 gram
    Directions:
    Prednisone, Taper 5 mg every 3 days,
    Finish in 2.5 weeks a
    Lialda - take 2 pill everyday for 1 month
    Refill: 2 times'''