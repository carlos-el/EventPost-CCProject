# Project documentation section.

### Abstract:
The idea for this project is to develop a microservices based application for the cloud.
It will provide a discovering and management system for social events along with the possiblility of programming email-based notification for the desired events as reminders.

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

 More information will be given as the course goes on.