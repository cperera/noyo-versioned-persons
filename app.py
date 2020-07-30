from flask import Flask, request, jsonify, send_file
from redis import Redis
import person

app = Flask(__name__, static_url_path='/', static_folder='public')

redis_host, redis_port = ('localhost',6379)
redisClient = Redis(host=redis_host, port=redis_port)

@app.route('/')
def root():
    #send_file('public/index.html')''
    return f'You have reached the Person API.\n'

@app.route('/status')
def status():
    return (
        f'Flask app {app} now running! \n'
        f'Redis is running: host:{redis_host} port:{redis_port}'
    )

@app.route('/person/<int:id>/v<int:version>')
def get_versioned_person(id,version):
    return "NOT YET IMPLEMENTED"

@app.route('/person/<id>', methods=['GET'])
def get_person(id):
    return "NOT YET IMPLEMENTED"

@app.route('/person/<id>', methods=['POST'])
def update_person(id):
    params = request.args
    if person.validate_person_dict(params):
        return person.Person.from_dict(params)
    else:
        return f'Required parameters: {person.Person.required_fields}'

@app.route('/person/<id>', methods=['DELETE'])
def delete_person(id):
    return "NOT YET IMPLEMENTED"

@app.route('/person/all', methods=['GET'])
def get_all_persons():
    """returns the current version of all person objects"""
    # note: should do this pipelined / as a generator if many persons.
    persons = list(person.all_persons())
    return jsonify(persons)

