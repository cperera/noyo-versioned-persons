from redis import Redis
import uuid

redis_host, redis_port = ('localhost',6379)
redisClient = Redis(host=redis_host, port=redis_port)

class Person:
    """person object"""
    required_fields = {'firstname','lastname','age','email'}
    def __init__(self, firstname, lastname, age, email, 
            *args, id=None, middlename=None):
        """ Create person object from given params"""
        self.rep = f'Person({firstname},{lastname},{age},{email},{middlename})'
        self.id = id # use a class method for next id? redis auto-assign?
        self.first = firstname
        self.middlename = middlename
        self.last = lastname
        self.age = age
        self.email = email
        if not self.id:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return self.rep

    def to_json(self):
        fields = Person.required_fields.union({'id','middlename'})
        var_dict = vars(self)
        return {key : var_dict[key] for key in vars(self) if key in fields}

    def new_redis_object(self,version=None):
        # creates a redis object for this class.
        if not version:
            version = get_current_version(self.id)
            if not version:
                version = 1
        person_key = redis_person_key(self.id,version)
        return f'NOT DONE: person_key: {person_key}'

    @classmethod
    def from_dict(cls,arg_dict):
        # ADDITIONAL VALIDATION REQUIRED 
        # sanitize arg strings before putting this in production
        return cls(**arg_dict)

# REDIS SECTION
def redis_person_key(id,version=None):
    if not version:
        current = get_current_version(id)
        if current:
            return f'Person::id:{id}::v:{current}'
        else:
            return f'Person::id:{id}::v:{current}'
    return f'Person::id:{id}::v:{version}'

def redis_version_key(id):
    return f'Person::id:{id}'

def get_current_version(id):
    return redisClient.get(redis_version_key(id))

def delete_person_by_id(id):
    version = get_current_version(id)
    redisClient.delete(redis_person_key(id,version))

    last_version = redisClient.decr(redis_version_key(id))
    return redisClient.delete()

def post_person(person_dict):
    print(f'attempting to POST person {person_dict}')
    valid,message = validate_person_dict(person_dict)
    if not valid:
        return message
    try:
        id = redisClient.get(person_dict)
        version = redisClient.incr()
    except Exception as e:
        print("encountered an exception!")
        raise e
    return

def all_persons():
    uuids = redisClient.smembers('person::uuidset')
    response_list = list(uuids)
    return response_list

def validate_person_dict(person_dict):
    for key in Person.required_fields:
        if key not in person_dict:
            return (False, f'missing param: {key}')
        elif key == "age" and not person_dict[key].isdigit():
            return (False, f'param age must be an integer in digits')
    return (True,'')

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
