from redis import Redis
import uuid

redis_host, redis_port = ('localhost',6379)
redisClient = Redis(host=redis_host, port=redis_port,decode_responses=True)

class Person:
    """person object"""
    required_fields = {'firstname','lastname','age','email'}
    allowed_fields = {'id','middlename'}
    def __init__(self, firstname, lastname, age, email, 
            *args, id=None, middlename=None):
        """ Create person object from given params"""
        self.rep = f'Person({firstname},{lastname},{age},{email},{middlename})'
        self.id = id # use a class method for next id? redis auto-assign?
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.age = age
        self.email = email
        if not self.id:
            self.id = str(uuid.uuid4())
        else:
            self.id = str(id)

    def __repr__(self):
        return self.rep

    def to_dict(self):
        fields = ['firstname','lastname','age','email','id','middlename']
        var_dict = vars(self)
        print(var_dict)
        return ({key : var_dict[key] for key in fields 
            if key in var_dict and var_dict[key]})

    def save_to_redis(self):
        # creates or updates a redis object for this class.
        version_key = redis_version_key(self.id)
        version = redisClient.incr(version_key)
        # note: if no version, version is set to 1
        redisClient.hset(redis_person_key(self.id, version),mapping=self.to_dict())
        redisClient.sadd('person::uuidset',version_key)
        return f'Success: {self} added at version:{version}'

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
            return f'person::id:{id}::v:{current}'
        else:
            return None
    return f'person::id:{id}::v:{version}'

def redis_version_key(id):
    return f'person::id:{id}'

def person_from_redis(id,version=None):
    rp_key = redis_person_key(id,version)
    if rp_key:
        arg_dict = redisClient.hgetall(redis_person_key(id))
        return Person.from_dict(arg_dict)
    else:
        return None
        
def to_dict(redis_dict):
    fields = Person.required_fields.union({'id','middlename'})
    return {key : redis_dict[key] for key in redis_dict if key in fields}

def get_current_version(id):
    return redisClient.get(redis_version_key(id))

def delete_person_by_id(id):
    version = get_current_version(id)
    if not version:
        return 0
    person_key = redis_person_key(id,version)
    version_key = redis_version_key(id)
    deleted = redisClient.delete(person_key)
    last_version = int(redisClient.decr(redis_version_key(id)))
    if last_version == 0:
        popped = redisClient.spop('persons', version_key)
        redisClient.delete(popped)
    return 1

# def post_person(person_dict):
#     print(f'attempting to POST person {person_dict}')
#     valid,message = validate_person_dict(person_dict)
#     if not valid:
#         return message
#     try:
#         id = redisClient.get(person_dict)
#         version = redisClient.incr()
#     except Exception as e:
#         print("encountered an exception!")
#         raise e
#     return

def all_persons():
    uuids = redisClient.smembers('person::uuidset')
    print(uuids)
    person_key_list = [redis_person_key(mem) for mem in uuids]
    print(person_key_list)
    response_list = [redisClient.hgetall(person) for person in person_key_list]
    print(response_list)
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
