# flask-docker
A python flask service which manages the lifecycle of a docker container.

## Supported APIs:
* `GET /start?name='friendly_name'` - used for starting the docker container. The `friendly_name` parameter is optional and in case it is not passed, a default name will be used.
* `GET /stop` - used for stopping the docker container.
* `GET /status` - used for retrieving the current status of the docker container.

## Assumptions
This app is built on top of the [docker-py](https://docker-py.readthedocs.org) project.

 1. This service is designed to run on Mac OS X. 

 2. A container that is already started and running cannot be started again unless it'll be stopped before.

 3. A container this is stopped and not running cannot be stopped again unless it'll be started before.

 4. There is **only one** available container, and hance only one unique container id. However, the given name is not fixed and might get different values each time the container is being started.
 
 5. The container's image has a very simple functionaliy - it hangs and waits for 60 seconds and then shuts down.

 
## How to run?
1. Make sure you have [boot2docker]() installed locally on your Mac and that you have configured the following https://docker-py.readthedocs.org/en/stable/boot2docker/.
2. Clone the repository.
3. Run `pip install -r requirements.txt -U` for installing all the dependencies.
4. Run `python app.py` (the service default port is 8081).


## Running tests
All you need to do is run the following:

`$ py.test tests.py --verbose`
