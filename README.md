# The App
## How do I run the app locally?
Flask app using redis as data store.

## Setup
1. install docker locally
1. install redis: `docker pull redis:6.0.6`
1. acivate virtual env: `source venv/bin/activate`
1. install requirements with `pip install -r requirements.txt`
1. start app using `flask run`
[ ] docker pull redis

## Testing

# Required Operations Checklist
| [x]  | Action          | Description            |
|------|-----------------|------------------------|
| [ ]  |          Create | -> insert person       |
| [ ]  |     Single Read | id -> person           |
| [ ]  | Version S. Read | id, ver -> person@ver  |
| [ ]  |        Read All | -> [person1, person2..]|
| [ ]  |          Update | id -> person@ver       |
| [ ]  |          Delete | id -> del person(id)   |

# Looking For:

- Your solution should meet the feature requirements laid out above
- The API should provide a reasonable amount of error handling on the inputs
- We should be able to run your solution locally - consider documentation or other
methods to make your code easier to run on a different machine
- Your solution should have some amount of testing


