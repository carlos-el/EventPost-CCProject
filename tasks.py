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
    c.run("docker ps -a | grep -q 'events'")
    c.run("docker ps -a | grep -q 'notifications'")

# builds and runs in bg the images with the microservices
@task
def buildContainers(c):
    c.config.run.shell = proper_shell
    c.run("docker-compose up -d")

# uploads the docker images created to Github repository registry 
@task
def uploadImageToGithub(c):
    c.config.run.shell = proper_shell
    c.run("env IMG_ID1=`docker images eventpost-ccproject_events_container -q`")
    c.run("env IMG_ID2=`docker images eventpost-ccproject_notifications_container -q`")
    c.run("echo 'Test variables'")
    c.run("docker images eventpost-ccproject_events_container -q")
    c.run("echo $IMG_ID1")
    c.run("echo $IMG_ID2")
    c.run("docker login docker.pkg.github.com -u carlos-el -p $GITHUB_ACCESS_TOKEN")
    c.run("echo 'Login done'")
    c.run("docker tag $IMG_ID1 docker.pkg.github.com/carlos-el/eventpost-ccproject/eventpost-ccproject_events_container:latest")
    c.run("docker tag $IMG_ID2 docker.pkg.github.com/carlos-el/eventpost-ccproject/eventpost-ccproject_notifications_container:latest")
    c.run("echo 'Tags done'")
    c.run("docker push docker.pkg.github.com/carlos-el/eventpost-ccproject/eventpost-ccproject_events_container:latest")
    c.run("docker push docker.pkg.github.com/carlos-el/eventpost-ccproject/eventpost-ccproject_notifications_container:latest")


# starts the server with the specified parameters
@task
def startServer(c, host, port, service):
    c.config.run.shell = proper_shell
    c.run("gunicorn -b %s:%s %s &" %(host, port, service))

