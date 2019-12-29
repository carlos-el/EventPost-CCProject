 # EventPost:
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)  
[![Build Status](https://travis-ci.com/carlos-el/EventPost-CCProject.svg?branch=master)](https://travis-ci.com/carlos-el/EventPost-CCProject)
[![CircleCI](https://circleci.com/gh/carlos-el/EventPost-CCProject.svg?style=svg)](https://circleci.com/gh/carlos-el/EventPost-CCProject)
[![Code coverage](https://codecov.io/gh/carlos-el/EventPost-CCProject/branch/master/graphs/badge.svg)](https://codecov.io/gh/carlos-el/EventPost-CCProject/branch/master)
[![DevQAGRX](https://img.shields.io/badge/DevQAGRX-blueviolet?style=svg&logo=Git)](https://github.com/JJ/curso-tdd)

The goal is to achieve a fully deployed system while using and learning continuous and incremental integration, cloud services and agile procedures in projects. 
Further information about the project is available in the __[documentation](https://carlos-el.github.io/EventPost-CCProject/index).__

## Requirements and Usage:

- Previous requirements: 
    - `Docker`
    - `python 3.6 - 3.8`
- Install: 
    - `pip3 install invoke`
    - `invoke installDependencies`
- Build: 
    - `invoke buildContainers`
- Test: 
    - `invoke test`
    - `testContainers`
- Coverage: 
    - `invoke coverage`
- Run: 
    - `invoke runContainers`

## Task tool used:
buildtool: tasks.py

More information ca be found [here](/docs/index.md#task-tool)

## Containers:
Contenedor: https://hub.docker.com/r/carlosel/eventpost-cc

A container has been deployed in Heroku: https://eventpost.herokuapp.com/events

More information about containers available [here](/docs/index.md#docker).

## Development:
We have added MongoDB as database for our 2 microservices (Events and Notifications). For this purpose several actions had been done:
- Created a new Dator in each microservice for managing access to the MongoDB database and use of the Single Source of Truth principle in the microservices resources. Links: [events dator file](/events_microservice/models/event_dator.py), [notifications dator file](/notifications_microservice/models/notification_dator.py). 
- Added the MongoDB installation in the dockerfiles so the database is local to the microservices. Links to dockerfiles [Events Dockerfile](./Events.dockerfile). [Notifications Dockerfile](./Notifications.dockerfile). More information about Docker use available [here](/docs/index.md#docker). 
- As we are using Gunicorn, 4 workers are used when starting the server.
- Created a python script for populating the database with basic resources. The script uses the URL where the service is hosted and the type of resources to populate the database with. The usage is the following: `python3 fixtures.py <url> <resource>`. It can be also used through the task tool. Link to the file: [fixtures.py](/fixtures.py)

## Optimization:
In order to achieve a good performance two actions have been performed:
-
- Gunicorn workers at server start up have been set to 7 (this is done in the [dockerfile](/Events.dockerfile) CMD command) in an attempt to be able to handle 10 cocache ncurrent user requests.
- A cache module called [falcon-caching](https://falcon-caching.readthedocs.io/en/latest/) has been added to the Falcon web framework in order to improve requests prosecution. It just requires setting the type of cache desired in the app module and adding a decorator to the resources classes.

## Performance testing:
Performance testing has been carried on using Taurus with Jmeter as executor. A [taurus script](/tests/performance/performance_testing.yml) has been creted for testing both microservices. The script contains auto-explainatory annotations but basically it consist of the following:
- Two scenarios for each microservice:
    - GET-Scenario: Performs one GET request to obtain all resources in the system, gets 5 ids of the resources obtained and performs a GET request to each of this specific ids. In total it contains a cycle of 6 GET request to hte microservice.
    - POST-PUT-DELETE Scenario: Makes a POST request to the microservice creating a new resource, then it retrieves the id of the new resource created abd performs a PUT and a DELETE request to this specific resource previously created. It Contains acycle of 3 requests, POST, PUT and DELETE, in taht order.   
- Taurus cache simulation is disabled for all scenarios so it does not give a better performance than it should.
- The execution section uses both scenarios of only one microservice at the same time trying to simulate a real load.
    - For the GET scenario we have used a throughput of 3000 and a concurrency of 7. For the POST-PUT-DELETE scenario we have used a throughput of 1000 and a concurrency of 3. 
        - In Taurus throughput and concurrency of scenarios executed at the same time stacks so finally we get a total throughput of 4000 (being 75% GET requests and 25% a mix of POST, PUT and DELETE requests) with a concurrency of 10. It tries to simulates the normal schema load that this microservice could receive in production. Notice that the throughput is set to 4000 so this does not become a limitation for the test.

Results obtained from performing this tests over the Events microservice in a local container, and after populating the database, prove that the microserve can hold up 10 concurrent users while maintaining over __2000 RPS and an average response time of 4ms.__ A deeper study about performance can be found [here](/docs/index.md#results).
