from invoke import task

@task 
def createdependencies(c):
    c.run("pip3 freeze > requirements.txt")

@task 
def installdependencies(c):
    c.run("pip3 install -r requirements.txt")

@task
def test(c):
    c.run("coverage run --source=events_microservice,notifications_microservice -m py.test")

@task
def coverage(c):
    c.run("coverage xml")
    c.run("codecov")
    