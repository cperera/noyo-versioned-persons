from redis import Redis

redis_host, redis_port = ('localhost',6379)
redis = Redis(host=redis_host, port=redis_port)

class Person:
    """person object"""
    @classmethod
    def from_dict(cls,arg_dict):
        return cls(**arg_dict)

    @classmethod
    def required_keys(cls):
        return set(['firstname','lastname','age','email'])

    def __init__(self, firstname, lastname, age, email, *args, middlename=None):
        self.rep = f'Person({firstname},{lastname},{age},{email},{middlename})'
        self.id = -1 # use a class method for next id? redis auto-assign?
        self.first = firstname
        self.middlename = middlename
        self.last = lastname
        self.age = age
        self.email = email

    def __repr__(self):
        return self.rep

    def redis_object(self,version=None):
        # creates a redis object for this class.
        if version == None:
            version = 1
        person_key = redis_person_key(self.id,ver)
        return "a string that redis can ingest?"

    def save(self):
        pass

# REDIS SECTION
def redis_person_key(id,version=None):
    if not version:
        current = get_current_version(id)
        if current:
            return f'Person::id:{id}::v:{current}'

def redis_version_key(id):
    return f'Person::id:{id}'

def get_current_version(id):
    return redis.get(redis_version_key(id))

def delete_person_by_id(id):
    version = get_current_version(id)
    redis.delete(redis_person_key(id,version))

    last_version = redis.decr(redis_version_key(id))
    return redis.delete()


def post_person(person_dict):
    print(f'attempting to POST person {person_dict}')
    if not validate_person_dict(person_dict):
        return
    try:
        id = redis.get()
        version = redis.incr()
    except Exception as e:
        print("encountered an exception!")
        raise e
    return 

def validate_person_dict(person_dict):
    for key in Person.required_keys():
        if key not in person_dict:
            return False
    return True

# for bulk operations, create a pipeline.
# possibly these should be a separate file.
def bulk_save_to_redis(person_list=[],filename=''):
    """takes a person_list or filename, loads objects into redis"""
    if not person_list and not filename:
        print('requires argument person_list or argument filename')
    print('NOT YET IMPLEMENTED')
    return

def bulk_load_from_redis(person_id_list):
    pass

def test_Person():
    bob = Person(
        firstname='Bob',
        lastname='Baratheon',
        age='43',
        email="n@nemail.com"
    )
    print(bob)
    print(bob.redis_object())

def test_Person_from_dict():
    test_dict = {
        "firstname":"Cob",
        "lastname":"Caratheon",
        "age":-10,
        "email":"n@nemail.com"
    }
    dictracy = Person.from_dict(test_dict)
    print(f'Person from dict: {dictracy}')
    print(
        f'redis_object from person from dict:'
        f'{dictracy.redis_object()}'
    )

def test_validate_person_dict():
    pass

def test_redis_create_and_delete():
    pass

def all_tests:
    test_Person()
    test_Person_from_dict()
    test_redis_create_and_delete():


