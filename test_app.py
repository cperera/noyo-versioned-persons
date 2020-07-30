import requests
import person

base_url = '127.0.0.1:5000/'
pdict_1 = {
    "firstname":"Cob",
    "lastname":"Caratheon",
    "age":1,
    "email":"n@nemail.com"
}
pdict_2 = {
    "firstname":"Rob",
    "lastname":"Caratheon",
    "age":12,
    "email":"n@nemail.com"
}
example_person = person.Person.from_dict(pdict_1)
example_person_update = person.Person.from_dict(pdict_2)

def all_tests():
    # these tests are meant to test the app by sending requests.
    # start the app before running this suite.
    assert (not test_delete()), "Deleting nonexistant person?"
    assert test_create(), "Could not create person"
    assert test_update(), "Could not update person"
    assert test_delete(), "Could not delete person"
    assert test_update_idempotence(), "Duplicate updates both bumped version!"

payload = {}
def test_delete():
    response = requests.delete(base_url+f'persons/{example_person.id}')
    return False

def test_create():
    return False

def test_update():
    return False

def test_update_idempotence():
    return False

def main():
    all_tests()
    
if __name__ == '__main__':
    main()