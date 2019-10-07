# Project documentation section.
### Abstract:
We will develop an applicaction for managing, discovering and browsing events.
* The user adressing the page willl be able to:
    - Create an account in our service.
    - Browse he page in order to find event of interest.
    - Program email-based notifications for different events. 
    - Manage email-based subscriptions to different feeds based on event topics.
    

* We will be using a microservices based arquitecture. The microservices needed and their specifications to achieve our goal are the following:
    - One for managing user accounts. Stores the users information and receives request for authentication and managing account. A RESTful API will be used for communication. Language and technology still to decide.
    - Another for managing events. Stores events information and receives request for managing events. A RESTful API will be used for communication. Language and technology still to decide.
    - A microservice for managin the notifications. Stores information relevant for the notifications and receives requests for managing them. Also uses a RESTful API for communication. Language and technology still to decide.
    - Other microservice for sending the emails requested by other services. Includes a queu of emails and send them in order. Therefore the communication protocol will be AMQP. We will develop it in Javascript using node.js and RabbitMQ as messaging middleware.
    - Finally and API Gateway is also needed as an interface for interacting with the microservices and authenticating users in different services.

 More information will be given as the course goes on.