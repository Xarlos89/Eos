## Flask
The Eos API is created using Flask.
We are using a standard flask API to localhost, with separate endpoints in Blueprints.
Blueprints can be found in api/routes

## Docker
The dockerfile is standard for a Flask API in docker. We run our app on localhost, using port 5000. It is connected to other services using the docker network defined in the Docker compose file