 # EventPost:
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)  
[![Build Status](https://travis-ci.com/carlos-el/EventPost-CCProject.svg?branch=master)](https://travis-ci.com/carlos-el/EventPost-CCProject)
[![CircleCI](https://circleci.com/gh/carlos-el/EventPost-CCProject.svg?style=svg)](https://circleci.com/gh/carlos-el/EventPost-CCProject)
[![Code coverage](https://codecov.io/gh/carlos-el/EventPost-CCProject/branch/master/graphs/badge.svg)](https://codecov.io/gh/carlos-el/EventPost-CCProject/branch/master)
[![DevQAGRX](https://img.shields.io/badge/DevQAGRX-blueviolet?style=svg&logo=Git)](https://github.com/JJ/curso-tdd)

The goal is to achieve a fully deployed system while using and learning continuous and incremental integration, cloud services and agile procedures in projects. 
Further information about the project and previous milestones is available in the __[documentation](https://carlos-el.github.io/EventPost-CCProject/index).__

### Architecture:
We will be using a microservices based architecture. The microservices needed arise from decomposing our system using Domain Driven Design subdomains. The microservices developed to achieve our goal, their specification, technologies and more architecture related information available [here](https://carlos-el.github.io/EventPost-CCProject/index#architecture).

### User stories and functionalities:
The user stories for the project and the functionalities derived from them that have been maped into porject milestones and issues can be found [here](https://carlos-el.github.io/EventPost-CCProject/index#user-stories).

## Continuous integration:
This section will describe the continuous integration system and tools, the testing and the building tool used.

### Testing:
A series of unitary test have been develop for our basic microservice entities. For testing the code the python library [pytest](https://docs.pytest.org/en/latest/contents.html) has been used. Another library, [coverage](https://coverage.readthedocs.io/en/v4.5.x/), has been also used for generating the testing coverage reports. Finally this information is uploaded to [CodeCov](https://codecov.io/) using its command tool.

Once we have created our test we can execute them, check the tests coverage, generate a report file and upload the report to CodeCov.

### Task tool:
buildtool: tasks.py

As we are using python the task tool selected has been [invoke](http://www.pyinvoke.org/). It uses the file [tasks.py](./tasks.py) for declaring tasks. In each task we can declare a series of cammands to execute. Finally we can do `invoke <task>` to carry out the desired task.

We created tasks for updating the dependencies file (requirements.txt), installing new dependencies, running test and creating coverage reports. Later on in the project we will be able to create tasks for building and deploying the project.

### CI tools:

For continuous integration we have used two different tools, Travis-CI and Circle-CI. For both of them to work we need to link our GitHub account to the services, allow access to the our repository and add a configuration file.

For TravisCI the file used is [.travis.yml](./.travis.yml). There we can specify the laguage versions to test and the commands for setting it up. In previous test we found out that the system does not work below python3.5 due to dependencies.

For CircleCI the file used is [config.yml](./.circleci/config.yml). The concept is the same as in the travis file but with a different sintax. More information about both files can be found in their links.

## Usage:

- Python version: `3.5 - latest`
- Install: `pip3 install -r requirements.txt`
- Test: `invoke test`
- Coverage: `invoke coverage`
