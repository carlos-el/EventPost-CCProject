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
    - `Python 3.6 - 3.8`
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
    - `invoke runContainers` (starts containers) or `invoke runAWS` (virtual machines provisioning in AWS)

## Task tool used:
buildtool: tasks.py

More information ca be found [here](/docs/index.md#task-tool)

## Containers:
Contenedor: https://hub.docker.com/r/carlosel/eventpost-cc

A container has been deployed in Heroku: https://eventpost.herokuapp.com/events

More information about containers available [here](/docs/index.md#docker).

## Performance testing:
Prestaciones: performance_testing.yml

More information about this available [here](/docs/index.md#performance-testing)

## Deployment to AWS EC2 using Ansible:
In this section we will describe how to deploy our dockerized application using AWS EC2 instances and Ansible to provide them. Steps for setting up Ansible and the AWS CLI so they can work together can be found [here](/docs/index.md#setting-up-aws-cli-and-ansible).

Once the development environment is ready we can create an Ansible file structure for provisioning. It will live in the provision folder. In our case we have choosen to use Ansible not only to provide the instances (2 instances, 1 for each microservice) but to instanciate them. Here are the microservices and how they have been deployed:

Link to deployed microservices in AWS using Ansible (they will be up until the end of the 1920 first term): 
- Events microservice: ec2-54-152-202-221.compute-1.amazonaws.com/events
- Notifications microservice: ec2-18-208-182-138.compute-1.amazonaws.com/notifications


### Use of Ansible:
- Firstly we have used ansible-vault for storing AWS credentials in a file that is not presdent in the repository. More information in the ['Setting up AWS and Ansible section'](/docs/index.md#setting-up-aws-cli-and-ansible).
- We have defined a __[configuration file](/ansible.cfg)__ in the root directory so it can be found by Ansible. Here we just state the directory of the ansible host inventory and the unkown hosts policy.
- Then we have created the __[hosts inventory file]__(/provision/hosts). It contains an empty host group where the EC2 instances created will be added at runtime. It also defines the private key to use when connecting to them and the default user.
- Two __tasks__ files have been created. One for [installing docker](/provision/roles/eventpost/tasks/install_docker.yml) in the instances and the other for [terminating instances](/provision/roles/eventpost/tasks/terminate_eventpost_instances.yml) previously created (EventPost instances will be marked using tags). Both of them are part of a __role__ defined in [main.yml](/provision/roles/eventpost/tasks/main.yml). It will be used in the provisioning playbook.
- The Ansible __playbook__ is the most interesting part. The full file with annotations can be found [here](/provision/provision.yml). Inside it we use 3 hosts directives as described below:
    - The first host directive:
        - Uses localhost (our machine).
        - Terminates old EventPost instances is there is any.
        - Starts two new instances with specific tags assigned so we can identify them later.
        - Adds the newly created instances DNS to an empty host group.
        - Waits until the instances can be addressed throught SSH.
    - The second host directive: 
        - Uses the in-memory host group created in by the localhost when starting the instances. also uses a user with privileges to interact with the instances.
        - Installs Docker in the virtual machines belonging to the host group.
        - Pulls a docker image to the instance (a different one depending on the microservice. Our Events instance will receive the events image, etc).
        - Starts a container using the previously pulled image (basically starts the service).
    - The third host directive:
        - Uses localhost again.
        - Checks the microservices ports until they are available.
        - Populates each microservice database with data.

### Describing the instances:
AWS EC2 service offers a good amount of configurations for its instances. The configuration that we have choosen for our microservices is the following:
- Instance type (hardware): We have decided to use __t2.xlarge__, it offers a decent performance (tested in the next section) for a good price, 0.185 USD/hour (can differ depending on the market) (Actually, for development and not wasting money we used t2.micro which is included in the free tier usage of the AWS EC2 service).
![t2 header](docs/img/t2_headers.png "t2 header")
![t2 specs](docs/img/t2.xlarge_specs.png "t2 specs")
- Image: As image we will be using UbuntuServer 18.04. By default, AWS does not offer many images for educational accounts and some of them are for specific use. Between the different options Ubuntu Server is a reliable and known to the developer. 
- Security group: In EC2 instances use a security group for managing which ports are open and who can address them. Using the AWS EC2 GUI conosle we have created a group that opens port 22 (SSH), 80 (HTTP) and 443 (HTTPS) to the world.
- Region: region where the instances should be created. For the educational account only 'us-east' is available. It would have been nice to deploy the services closer to Spain for latency but we had no choice.

## AWS EC2 instance performance testing:
For testing the performance of the microservices we have used __t2.xlarge__ EC2 instances and the Taurus scripts created for the previous milestone. More information about this test can be found [here](/docs/index.md#AWS-EC2-Instances-performance-testing).

We have tested executing the script from our local computer addressing the instance and executing the script in the same machine (instance) the service is deployed on.

When executing the script using our local computer the RPS were horrible as well as the latency (the region where the instances are deployes is 'us-east').
But when executing the test in the same instance we obtained a result of 1224 which is quite good for the cost of the machine.
