from invoke import task
import os

proper_shell = os.getenv("SHELL")

# updates dependencies file
@task 
def createDependencies(c):
    c.config.run.shell = proper_shell
    c.run("pip3 freeze > requirements.txt")

# updates dependencies in the system
@task 
def installDependencies(c):
    c.config.run.shell = proper_shell
    c.run("pip3 install --upgrade pip")
    c.run("pip3 install -r requirements.txt")

# runs tests and check coverage 
@task
def test(c):
    c.config.run.shell = proper_shell
    c.run("coverage run --source=events_microservice,notifications_microservice -m py.test")

# create coverage report and uploads it to codecov
@task
def coverage(c):
    c.config.run.shell = proper_shell
    c.run("coverage xml")
    c.run("codecov")

# installs docker-compose
@task
def installDockerCompose(c):
    c.config.run.shell = proper_shell
    c.run("curl -L https://github.com/docker/compose/releases/download/1.25.0/docker-compose-`uname -s`-`uname -m` -o docker-compose")
    c.run("chmod +x docker-compose")

# tests that the containers have been created
@task
def testContainers(c):
    c.config.run.shell = proper_shell
    c.run("docker images | grep 'events_container'")
    c.run("docker images | grep 'notifications_container'")

# builds and the images with the microservices
@task
def buildContainers(c):
    c.config.run.shell = proper_shell
    c.run("docker build -f Events.dockerfile -t events_container .")
    c.run("docker build -f Notifications.dockerfile -t notifications_container .")

# runs in bg the containers with the microservices
@task
def runContainers(c):
    c.config.run.shell = proper_shell
    c.run("docker run --rm -dit -p 8000:8080 events_container")
    c.run("docker run --rm -dit -p 8001:8080 notifications_container")

# uploads the docker images created to Github repository registry 
@task
def uploadImageToGithub(c):
    c.config.run.shell = proper_shell
    c.run("docker login docker.pkg.github.com -u $GITHUB_USER -p $GITHUB_ACCESS_TOKEN")
    c.run("docker tag `docker images events_container -q` docker.pkg.github.com/carlos-el/eventpost-ccproject/events_container:latest")
    c.run("docker tag `docker images notifications_container -q` docker.pkg.github.com/carlos-el/eventpost-ccproject/notifications_container:latest")
    c.run("docker push docker.pkg.github.com/$GITHUB_USER/events_container:latest")
    c.run("docker push docker.pkg.github.com/$GITHUB_USER/notifications_container:latest")

# starts the server with the specified parameters
@task
def startServer(c, host, port, service):
    c.config.run.shell = proper_shell
    c.run("gunicorn -b %s:%s %s &" %(host, port, service))

@task 
def populateHerokuEventsApp(c):
    c.run("python3 fixtures.py https://eventpost.herokuapp.com/events events")
