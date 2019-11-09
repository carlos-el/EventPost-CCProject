from invoke import task

# updates dependencies file
@task 
def createdependencies(c):
    c.run("pip3 freeze > requirements.txt")

# updates dependencies in the system
@task 
def installdependencies(c):
    c.run("pip3 install -r requirements.txt")

# runs tests and check coverage 
@task
def test(c):
    c.run("coverage run --source=events_microservice,notifications_microservice -m py.test")

# create coverage report and uploads it to codecov
@task
def coverage(c):
    c.run("coverage xml")
    c.run("codecov")
    