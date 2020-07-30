import requests
from urllib import parse
import person

base_url = 'http://127.0.0.1:5000/'
example_uuid = 'b04bb301-0f7c-4937-8f83-88e05dd80098'
pdict_1 = {
    "firstname":"Cob",
    "lastname":"Caratheon",
    "age":1,
    "email":parse.quote("n@nemail.com")
}
pdict_2 = {
    "firstname":"Rob",
    "lastname":"Caratheon",
    "age":12,
    "email":parse.quote("n@nemail.com")
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

def test_delete():
    response = requests.delete(base_url+f'person/{example_person.id}')
    print(f'delete person {example_person.id}: status {response.status_code}')
    if response.status_code == 200:
        return True
    else:
        return False

def test_create():
    response = requests.post(base_url+f'person',params=pdict_1)
    print(f'status: {response.status_code}')
    return response.status_code == 200

def test_read():
    response = requests.get(base_url+f'person/{example_person.id}')
    return response.status_code==200

def test_read_versioned():
    response = requests.get(base_url+f'person/{example_person.id}/1')
    return response.status_code==200

def test_update():
    uuid = 'b04bb301-0f7c-4937-8f83-88e05dd80098'
    response = requests.post(base_url+f'person/{example_uuid}',params=pdict_2)
    return response.status_code==200

def test_update_idempotence():
    response = requests.post(base_url+f'person/{example_person.id}',params=pdict_1)
    assert status_code==200, 'first idempotence update failed'
    first_person_version = person.redis_person_key(example_person.id)
    assert status_code==200, 'duplicate idempotence update failed'
    response = requests.post(base_url+f'person/{example_person.id}',params=pdict_1)
    next_person_version = person.redis_person_key(example_person.id)
    return first_person_version == next_person_version

def main():
    all_tests()
    
if __name__ == '__main__':
    main()