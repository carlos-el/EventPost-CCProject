# Project documentation section.

### Abstract:
The idea for this project is to develop a microservices based application for the cloud.
It will provide a discovering and management system for social events along with the possiblility of programming email-based notification for the desired events as reminders.

## Usage:

- Previous requirements: `Docker`
- Python version: `3.5 - latest`
- Install: 
    - `pip3 install invoke`
    - `invoke installDependencies`
    - `invoke installDockerCompose`
- Build: `invoke buildContainers`
- Test: 
    - `invoke test`
    - `testContainers`
- Coverage: `invoke coverage`

## Architecture:
As stated before, we will be using a microservices based architecture with one microservice per entity in the system and one as task dispatcher. The microservices needed arise from decomposing our system using Domain Driven Design subdomains. The microservices developed to achieve our goal are the following:
- Events: Stores events information and receives requests for managing events. 
- Notifications: Stores information relevant for the notifications and receives requests for managing them.
- Email-sender: Sends emails to the users when requested by other services. It will provide the functionality for sending the notification emails and other emails related to the system such as welcome emails for new accounts.

Addtionally we will use a service for user management.
- Users Management: Stores the users' information and receives requests for authentication and managing accounts. 

All of them will be addressed through a specific API Gateway. It will also be in charge of authenticating certain request to other microservices against the User management service.

A centralized system using Consul will take care of service discovery and configuration between microservices. There will be a centralized log system as well.

Finally, for queueing tasks to the Email-sender microservice a RabbitMQ instace will be deployed with the Email-sender as receiver. 

### Communication:

The majority of the communications will take place over HTTP. The user will be able to contact our microservices through the API Gateway RESTful API. The Gateway will route those messages to the User management, Events and Notifications microservices which will include a RESTful API for receiving messages.

Communication between the Email-sender and other microservices will be carried out using a RabbitMQ message broker implementing a queue and the AMQP protocol for message passing. The Email-sender will act as the receiver, taking messages from the queue and the other microservices will act as senders sending tasks to the queue.

### Database management:
In our system we will store the following data:
- Users data for authentication and user management (passwords, usernames, emails.)
- Events data (title, descriptions, date, time, place, topic).
- Notifications data (destination email, subject, content, scheduled time, event associated.)

In order to keep services independent, a Database-per-service architecture will be implemented. Each database will be private to its corresponding microservice. As there are no relation in our databases a NoSQL database will be used.

### Technologies:
- The __microservices__ will consist in the following:
    - Email-sender microservice will be implemented using NodeJS. This microservice is only intended for performing the task of sending emails and only communicates with the other system components through message broker. Therefore the only npm libreries needed for it are [amqplib](https://www.npmjs.com/package/amqplib) and [nodemailer](https://nodemailer.com/about/) which are widely known and easy to use.
    - The Users Management service and Events and Notification microservices will be implemented in Python. [Falcon](https://falconframework.org/) will be used as framework for working with HTTP RESTful requests and responses. It has been chosen for being a light-weight microframework written in Python that supports the REST architectural style. It is not suitable for serving HTML but this will not be a problem in our case. Our microservices have to send tasks over the AMQP protocol to a message broker, for this reason they will also use the library [pika](https://pypi.org/project/pika/) as it is designed for RabbitMQ brokers like the one that we are going to deploy.

- The __API Gateway__ will be deployed used [Express Gateway](https://www.express-gateway.io/) which uses NodeJS. It is one of the few API Gateways for NodeJS, it is simple, for general purpose and allows the fast development lifecycle required in agile projects.

- Our centralized system for __configuration and service discovery__ across microservices will be established using [Consul](https://www.consul.io/discovery.html) because it is designed especially for this task, it is easy to deploy and configure and it comes almost ready to work. It also supports containers.  

- For our __logging system__ we will be using [Loggly](https://www.loggly.com/), a SaaS platform that will provide an already deployed realiable enviroment for our logs. 

- For the __message broker__ we will use [CloudAMQP](https://www.cloudamqp.com/). It is a platform that offers RabbitMQ instances as a service and it also has free plans that cover our needs for this project. This will save us work when developing the deployment chain.

- As the __storage__ needed for our microservices consist on NoSQL databases, some of them with a consisten amount of data, we are going to use [MongoDB](https://www.mongodb.com/es). MongoDB is a document database which pairs quite well with the information needed to store events where we need a single object and joins will not going to be used. The [pymongo](https://api.mongodb.com/python/current/) library will be used in our python microservices so they can connect with the database.

#### Arquitecture basic diagram.
![Microservices architecture diagram](img/eventpost_architecture_diagram_v3.png "Microservices architecture diagram")

## User stories:
The user stories that came up are the following.
- As user I want to create an account so I can keep track of the events I like.
- As user I want to be able to look for events related to my likes, events near me so I do not have to make a trip and events that are going to take place next week so I can make a schedule.
- As an administrator I want to be able to manage events information so in case an event date change a can edit it.
- As user I would like to set reminder notifications of events I like and schedule a certain date and time for them so in case I have to buy tickets I can do it on time.
- As user I would like to be able to change the mail where the remainder notification is going to be send.  
- As user I want to receive notification on time so I do not mess up my schedule and add delay notifications in case I change my mind.  

##### System functionality:
The features found out in the user stories for each microservice have been mapped into milestones and its corresponding issues (links to milestones below). 
- [Events](https://github.com/carlos-el/EventPost-CCProject/milestone/6):
    -   Get events related to a topic.
    -   Get events happening in a range of time.
    -   Get events happening in a specified location.
    -   Get information of a certain event.
    -   Create an event.
    -   Delete an event.
    -   Edit an event.
- [Notifications](https://github.com/carlos-el/EventPost-CCProject/milestone/7):
    -   Create a notification.
    -   Get the notifications related to an account.
    -   Update the scheduled date and time of a notification.
    -   Update the email where a notification is going to be send.
    -   Delete a notification. 
- [Email-sender](https://github.com/carlos-el/EventPost-CCProject/milestone/8): 
    -   Send email notifications.

Additionally the User management system will include the following features.
[Users Management](https://github.com/carlos-el/EventPost-CCProject/milestone/5):
    -   Create an account.
    -   Delete an account.
    -   Update email.
    -   Add a secondary email to an account.

This features has been mapped into milestones and issues.

## Continuous integration:
This section will describe the continuous integration system and tools, the testing and the building tool used.

### Testing:
A series of tests have been develop for our microservices. For testing the code the python library [pytest](https://docs.pytest.org/en/latest/contents.html) has been used. Another library, [coverage](https://coverage.readthedocs.io/en/v4.5.x/), has been also used for generating the testing coverage reports. Finally this information is uploaded to [CodeCov](https://codecov.io/) using its command tool.

For implementing integration tests for the REST services we have used pytest and a Falcon feature, a [testing client](https://falcon.readthedocs.io/en/stable/api/testing.html) that lets us send requests to the server without starting it.

Once we have created our test we can execute them, check the tests coverage, generate a report file and upload the report to CodeCov.

### Task tool:
buildtool: tasks.py

As we are using python the task tool selected has been [invoke](http://www.pyinvoke.org/). It uses the file [tasks.py](./tasks.py) for declaring tasks. In each task we can declare a series of cammands to execute. Finally we can do `invoke <task>` to carry out the desired task.

We created tasks for updating the dependencies file (requirements.txt), installing new dependencies, running tests, building running and testing microservices containers, etc. All tasks can be found in the file [tasks.py](./tasks.py).

### CI tools:

For continuous integration we have used two different tools, Travis-CI and Circle-CI. For both of them to work we need to link our GitHub account to the services, allow access to the our repository and add a configuration file.

For TravisCI the file used is [.travis.yml](./.travis.yml). There we can specify the laguage versions to test and the commands for setting it up. In previous test we found out that the system does not work below python3.5 due to dependencies.

For CircleCI the file used is [config.yml](./.circleci/config.yml). The concept is the same as in the travis file but with a different sintax. More information about both files can be found in their links.

## Performance:
### Images :
Load performance measurements between containers using the Event microservice with 2 different base images (alpine and python:3.7-alpine) has been done. For this purpose we have used the tool [Taurus](https://gettaurus.org/) and used a reference [script with some modifications](/tests/performance/taurus_script.yml). Explanation about the script can be found in the in-line comments of the file. 

The tests have been performend in local using a Intel Core i7-4790 CPU @ 3.60GHz × 8 CPU. 

After pulling the required base images we have used this [dockerfile](/Dockerfile.events), changing only the FROM directive between alpine and python:3.7-alpine and deleting the python install line. Making this we creates 'events' image, with alpine and 'events-second' with 'python:3.7-alpine'.

![Docker images for testing](img/perf_comparison_images.png "Docker images for testing")
As we can see the image created with 'python:3.7-alpine' doubles the size of the other which is undesirable.
Now we will run the microservice and perform a load test in both containers.
![Containers up image](img/perf_comparison_containers.png "Containers up image")
Measurements for 'events' image (base image: alpine):
![events image (alpine) measurements](img/perf_comparison_results_alpine.png "events image (alpine) measurements")
Measurements for 'events-second' image (base image: python:3.7-alpine):
![events-second image (python:3.7-alpine) measurements](img/perf_comparison_results_python:alpine.png "events image (alpine) measurements")

For the same load we can see that the container using alpine as base image performs slightly better in terms of RPS and also has a slightly lower response time. With this metrics we can then assure than the 'alpine' base image is better for our project.

## Deployment:
### Heroku:
The Events microservice has been deployed to Heroku. The steps followed can be found in the [official documentation](https://devcenter.heroku.com/articles/git#prerequisites-install-git-and-the-heroku-cli), basically we just created a heroku app using the CLI, specify that it will be a containerized app and pushed our code to heroku. Additionally we have created a [heroku.yml](/heroku.yml) and enabled autodeploy for our app in order re-deploy the app everytime we make a push to our repository.
