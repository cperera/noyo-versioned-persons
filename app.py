from flask import Flask, request, jsonify, send_file, make_response, redirect, url_for
from redis import Redis
import person

app = Flask(__name__, static_url_path='/', static_folder='public')

redis_host, redis_port = ('localhost',6379)
redisClient = Redis(host=redis_host, port=redis_port,decode_responses=True)

@app.route('/')
def root():
    #send_file('public/index.html')''
    return (
        f'You have reached the Person API.'
        f' <ul><li> /person/&ltuuid&gt - [GET,POST,DELETE]</li>'
        f' <li> /person/&ltuuid&gt/&ltversion&gt - [GET]</li>'
        f' <li> /person/all/ - [GET]</li></ul>'
        f' <li> /person - [POST]</li> '
        )

@app.route('/status')
def status():
    return (
        f'Flask app {app} now running! \n'
        f'Redis is running: host:{redis_host} port:{redis_port}'
    )

@app.route('/person/all/', methods=['GET'])
def get_all_persons():
    """returns the current version of all person objects"""
    # note: should do this pipelined / as a generator if many persons.
    print('get_all_persons')
    persons = list(person.all_persons())
    return jsonify(persons)

@app.route('/person/<uuid:id>/<int:version>')
def get_versioned_person(id,version):
    print(f'ID WAS {id}, V WAS {version}, get_versioned_person')
    p = person.person_from_redis(id,version)
    return jsonify(p.to_dict())

@app.route('/person/<uuid:id>', methods=['GET'])
def get_person(id):
    print(f'ID WAS {id}, get_person')
    p = person.person_from_redis(id)
    return jsonify(p.to_dict())

@app.route('/person', methods=['POST'])
def create_person():
    print(f'Attempt to create_person')
    params = request.args
    # this logic should move to person.py
    if person.validate_person_dict(params):
        p = person.Person.from_dict(params)
        saved = p.save_to_redis()
        print(saved)
        return redirect(url_for('get_person',id=p.id))
    else:
        resp = make_response(f'Required parameters: {person.Person.required_fields}',400)
        return resp

@app.route('/person/<uuid:id>', methods=['POST'])
def update_person(id):
    print(f'ID WAS {id}, update_person')
    params = request.args.copy()
    params['id'] =str(id)
    # this logic should move to person.py
    if person.validate_person_dict(params):
        p = person.Person.from_dict(params)
        old_p = person.person_from_redis(params['id'])
        if (p and old_p) and p.to_dict() == old_p.to_dict():
            return f'person with id {id} was unchanged, no version bump'
        else:
            saved = p.save_to_redis()
            print(saved)
            return redirect(url_for('get_person',id=p.id))
    else:
        resp = make_response(f'Required parameters: {person.Person.required_fields}',400)
        return resp

@app.route('/person/<id>', methods=['DELETE'])
def delete_person(id):
    print(f'ID WAS {id}, delete_person')
    deleted = person.delete_person_by_id(id)
    if deleted:
        return f'Person with id {id} deleted.'
    else:
        return f'no such person with id {id}.'


