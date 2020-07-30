#from unittest.mock import Mock
from person import Person

### TESTS
# samples
bob = Person(
        firstname='Bob',
        lastname='Baratheon',
        age='43',
        email="n@nemail.com"
)
invalid = {'firstname':'mac'}
valid = {
    "firstname":"Cob",
    "lastname":"Caratheon",
    "age":1,
    "email":"n@nemail.com"
}
valid_with_extra = {
    "firstname":"Cob",
    "lastname":"Caratheon",
    "middlename":"Mollywobbles",
    "age":-10, # perhaps some age validation would be in order...
    "email":"n@nemail.com",
    "favorites":"math"
}

def test_person():
    print(bob)
    print(bob.new_redis_object())

def test_person_from_dict():
    test_dict = {
        "firstname":"Cob",
        "lastname":"Caratheon",
        "age":-10,
        "email":"n@nemail.com"
    }
    dict_person = Person.from_dict(test_dict)
    print(f'Person from dict: {dict_person}')
    print(
        f'redis_object from person from dict:'
        f'{dict_person.new_redis_object()}'
    )

def test_validate_person_dict():
    print(f'validate(invalid) -> {validate_person_dict(invalid)}')
    print(f'validate(valid) -> {validate_person_dict(invalid)}')
    print(f'validate(valid_with_extra) -> '
        f'{validate_person_dict(valid_with_extra)}')

def test_redis_create_and_delete():
    pass

def all_tests():
    test_person()
    test_person_from_dict()
    test_redis_create_and_delete()


