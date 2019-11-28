 # EventPost:
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)  
[![Build Status](https://travis-ci.com/carlos-el/EventPost-CCProject.svg?branch=master)](https://travis-ci.com/carlos-el/EventPost-CCProject)
[![CircleCI](https://circleci.com/gh/carlos-el/EventPost-CCProject.svg?style=svg)](https://circleci.com/gh/carlos-el/EventPost-CCProject)
[![Code coverage](https://codecov.io/gh/carlos-el/EventPost-CCProject/branch/master/graphs/badge.svg)](https://codecov.io/gh/carlos-el/EventPost-CCProject/branch/master)
[![DevQAGRX](https://img.shields.io/badge/DevQAGRX-blueviolet?style=svg&logo=Git)](https://github.com/JJ/curso-tdd)

The goal is to achieve a fully deployed system while using and learning continuous and incremental integration, cloud services and agile procedures in projects. 
Further information about the project and previous milestones is available in the __[documentation](https://carlos-el.github.io/EventPost-CCProject/index).__

## Docker
This section will describe how the use of docker has been added to our system and how it benefits from it.

#### Development:
In order to really show the Docker potential we have advanced in the development of our microservices. The Events and Notifications microservices have their main functionality implemented. It is possible to make CRUD operations over their resources using RESTful requests. For providing data to the resources we have created dators (actually mockers) that are injected into the resources.
The issues related to user stories that had been closed with this update: [#29](https://github.com/carlos-el/EventPost-CCProject/issues/29), [#30](https://github.com/carlos-el/EventPost-CCProject/issues/30), [#31](https://github.com/carlos-el/EventPost-CCProject/issues/31), [#32](https://github.com/carlos-el/EventPost-CCProject/issues/32), [#34](https://github.com/carlos-el/EventPost-CCProject/issues/34), [#35](https://github.com/carlos-el/EventPost-CCProject/issues/35), [#36](https://github.com/carlos-el/EventPost-CCProject/issues/36)


The choosen server has been [gunicorn](https://gunicorn.org/) using [Falcon](https://falconframework.org/) as microframework. For making the integration tests on the server resources we have used pytest and a Falcon feature, a testing client that lets us send requests to the server without starting it.

### Docker use:
The base image choosen for the containers has been alpine. Its really light allowing a fast development, test and deployment and also its quite popular so we can easily solve problems (we had to resolve some problems in invoke as the alpine shell is not bash but sh).

We have until now 2 microservices so we will be running 2 containers. Both containers will be created using a single parametrized Dockerfile. [Link to Dockerfile](./Dockerfile)

The Dockerfile does the following:
- Pulls the selected docker image.
- Declares 2 arguments to be used, SERVICE (name of the service) and PORT (port used to start the service) and exposes the port specified.
- Copies the files needed for the service in a directory and sets it as working directory. In order to copy only the strictly needed files a [.dockerignore](./.dockerignore) has been used.
- Updates and installs dependencies.
- Defines an entrypoint for starting the serven when the container is created.

For creating 2 different images with a single dockerfile we have used docker-compose. [Link to docker-compose file](./docker-compose.yml).

The docker-compose file does the following twice, one for each microservice:
- Specifies the name of the image.
- Sets the image context and the location of the dockerfile to use.
- Pass to the dockerfile 2 arguments that it takes form environment variables.
- Specifies the host-container port mapping.

When the docker-compose file is executed using `docker-compose up -d` with success both microservices will be ready to receive requests.

The links to the containers are the following:
Contenedor: https://github.com/carlos-el/EventPost-CCProject/packages/63507
Contenedor: https://github.com/carlos-el/EventPost-CCProject/packages/63509


#### Task tool (invoke):
buildtool: tasks.py
New commands have been added to the [task tool](./tasks.py). The new functionalities include:
- Installing docker-compose.
- Building the images and the containers for our microservices.
- Testing that the images have been created the right way after executing 'docker-compose up'.
- Uploading the docker images created with 'docker-compose up' to GitHub registry.
- Starting microservices server.

#### CI tools update:
In the [travis file](./.travis.yml), in the install section we have added one command for installing docker-compose and other for building the images and the containers with docker-compose.
In the script section we have added an order for testing the container and finally in the after_success section a command for uploading the docker images created to GitHub. All commands are invoke tasks.

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
