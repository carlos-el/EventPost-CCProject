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

# installs docker_compose
@task
def installDockerCompose(c):
    c.config.run.shell = proper_shell
    c.run("curl -L https://github.com/docker/compose/releases/download/1.25.0/docker-compose-`uname -s`-`uname -m` -o docker-compose")
    c.run("chmod +x docker-compose")

# starts the server with the specified parameters
@task
def startServer(c, host, port, service):
    c.config.run.shell = proper_shell
    c.run("gunicorn -b %s:%s %s &" %(host, port, service))
