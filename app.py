from flask import Flask, request, send_file
from redis import Redis
import person

app = Flask(__name__, static_url_path='/', static_folder='public')

redis_host, redis_port = ('localhost',6379)
redis = Redis(host=redis_host, port=redis_port)

@app.route('/')
def root():
    #send_file('public/index.html')''
    return f'You still need to make root html, my friend.'

@app.route('/status')
def status():
    return (
        f'Flask app {app} now running! \n'
        f'Redis is running: host:{redis_host} port:{redis_port}'
    )

@app.route('/parse/<query>/')
def parse(query):
    return f'Query: {query}. You still need to make query parser, my friend.'

@app.route('/person/<int:id>/v<int:version>')
def get_versioned_person(id,version):
    return "NOT YET IMPLEMENTED"

@app.route('/person/<int:id>',methods=['GET'])
def get_person(id):
    return "NOT YET IMPLEMENTED"

@app.route('/person/<int:id>',methods=['POST'])
def update_person(id):
    return "NOT YET IMPLEMENTED"

