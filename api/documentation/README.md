# Communicate with API
Main route: "http://localhost:5050"
```
1. Create new user:
    Route: "/user"
    Method: POST
    Input: {"first_name":<string>, "last_name":<string>, "password":<string>, "email":<string>}
    Output: On_Success- status code 200, {'message': user details}
            On_Failure- { 
                            1. status code 400, {'message': 'Error! ID already exists'} # duplicate id
                            2. status code 400, {'message': 'Error! Email already exists'} # duplicate email address
                            3. status code 500, {'message': 'ERROR!'} # other
                        }

2. Get existing user:
    Route: "user/<int:id>" # Replace <int:id> with id integer of requested user
    Method: GET
    Input: None
    Output: On_Success- status code 200, {'message': user details}
            On_Failure- {
                            1. status code 400, {'message': 'ERROR! user id not found'} # if given id not in DB
                            2. status code 500, {'message': 'ERROR!'} # other
                        }

3. Update existing user:
    Route: "user/<int:id>" # Replace <int:id> with id integer of requested user
    Method: PUT
    Input: {"first_name":<string>, "last_name":<string>, "password":<string>, "email":<string>}
    Output: On_Success- status code 200, {'message': user details}
            On_Failure- {
                            1. status code 400, {'message': 'ERROR! user id not found'} # if given id not in DB
                            2. status code 500, {'message': 'ERROR!'} # other
                        }

4. Delete existing user:
    Route: "user/<int:id>" # Replace <int:id> with id integer of requested user
    Method: DELETE
    Input: None
    Output: On_Success- status code 200, {'message': user id}
            On_Failure- {
                            1. status code 400, {'message': 'ERROR! user id not found'} # if given id not in DB
                            2. status code 500, {'message': 'ERROR!'} # other
                        }
