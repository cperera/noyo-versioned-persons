# The App
## How do I run the app locally?
Flask app using redis as data store.

## Setup - potentially??
1. install docker locally
1. install redis: `docker pull redis:6.0.6`
1. create virtual env: `python3 -m venv venv`
1. activate virtual env: `source venv/bin/activate`
1. install requirements with `pip install -r requirements.txt`
1. start app using `flask run`
[ ] docker pull redis

## Testing

# Person objects
A [`Person`](person.py) should have the following properties:
| - [ ]  | NAME        | DATA TYPE          |
|--------|-------------|--------------------|
| - [ ]  | ID          | (choice: UUID4)    |
| - [ ]  | First Name  | string             |
| - [ ]  | Middle Name | string, optional   |
| - [ ]  | Last Name   | string             |
| - [ ]  | Email       | string             |
| - [ ]  | Age         | integer            |

in redis, we will have
`Person` versioned objects as hashes
- HSET(`person::id:<id>::v:<version>`: first, last, email, age[, middle])

and keys that track current version:
- INCR(`person::id:<id>`)

when deleting, delete current version of this `Person` object
- DECR(`person::id:<id>`)
- 

then decrement its version (the value at key )

and finally, a set that keeps all the 

when person.delete_all (this is extra) delete all versions of this
between current version and version 0 inclusive. Then, delete the
key that tracks the current version.


# Required Operations Checklist
| - [x]  | Action          | Description            |
|--------|-----------------|------------------------|
| - [ ]  |          Create | -> insert person       |
| - [ ]  |     Single Read | id -> person           |
| - [ ]  | Version S. Read | id, ver -> person@ver  |
| - [ ]  |        Read All | -> [person1, person2..]|
| - [ ]  |          Update | id -> person@ver       |
| - [ ]  |          Delete | id -> del person(id)   |



# Looking For:

- Your solution should meet the feature requirements laid out above
- The API should provide a reasonable amount of error handling on the inputs
- We should be able to run your solution locally - consider documentation or other
methods to make your code easier to run on a different machine
- Your solution should have some amount of testing

# extras
This should be fine if we are using redis locally. Consider using pipelining,
or another batching solution?, for bulk operations. Consider using tornado + 
something like tornadis https://github.com/votem/toredis if need better network 
i/o characteristics?

Try to turn the return types that could be huge into generators?


