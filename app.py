from flask import Flask, request
from docker import Client
from docker.utils import kwargs_from_env

app = Flask(__name__)

# initialising the docker client assuming it's running on mac OS X
kwargs = kwargs_from_env()
kwargs['tls'].assert_hostname = False
docker_client = Client(**kwargs)
container = docker_client.create_container(
    image='busybox:latest',
    command='/bin/sleep 60')
container_id = container.get('Id')  # we have only one conatiner


@app.route('/start', methods=['GET'])
def start_docker():
    name = request.args.get('name')
    container_name = 'DEFAULT_NAME' if (name is None) else name
    status = get_container_status()
    if (status is None):
        docker_client.start(container_id)
        return "started docker container with id {} and name {}".format(
            container_id, container_name)
    return "container with id {} is already running".format(container_id)


@app.route('/stop', methods=['GET'])
def stop_docker():
    status = get_container_status()
    if (status is not None):
        docker_client.stop(container=container_id)
        return "stopped docker container with id {}".format(container_id)
    return "container with id {} is already not running".format(container_id)


@app.route('/status', methods=['GET'])
def get_status_docker():
    if (get_container_status() is None):
        return "Container is currently not running. Please hit /start API."
    status = get_container_status()
    return "docker container status is {}".format(status)


"""
Helper function for retrieving the status of the single container.
If there's no container avaialable (stopped or not even started), None is
being returned.
"""
def get_container_status():
    if (len(docker_client.containers()) > 0):
        return docker_client.containers()[0]['Status']
    return None

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)
