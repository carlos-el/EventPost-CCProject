# Scripts for populating databases of our microservices
import sys
import json
import requests 

# Define implemented fixtures
allowed_fixtures = ['events', 'notifications']

# Check the correct usage of the script
if len(sys.argv) is not 3 or sys.argv[2] not in allowed_fixtures:
    print('Allowed fixtures: ' + str(allowed_fixtures))
    print('Usage: "python3 fixtures.py <url> <fixture>"')
    exit(1)

# Get URL to send requests and fixture needed from command line parameters.
URL = sys.argv[1]
fixture = sys.argv[2]

# Creates events
def define_events_fixture():
    elements = []

    elements.append(json.dumps({"title": "Title test 1", "description": "Description 1, testing "+'a'*23, "date": "2020-12-12", "time": "20:50:12"}))
    elements.append(json.dumps({"title": "Title test 2", "description": "Description 2, testing "+'a'*23, "date": "2020-12-12", "time": "20:50:12"}))
    elements.append(json.dumps({"title": "Title test 3", "description": "Description 3, testing "+'a'*23, "date": "2020-12-12", "time": "20:50:12"}))
    elements.append(json.dumps({"title": "Title test 4", "description": "Description 4, testing "+'a'*23, "date": "2020-12-12", "time": "20:50:12"}))
    elements.append(json.dumps({"title": "Title test 5", "description": "Description 5, testing "+'a'*23, "date": "2020-12-12", "time": "20:50:12"}))
    
    return elements

#Cretes notifications
def define_notifications_fixture():
    elements = []

    elements.append(json.dumps({"subject": "Subject test 1", "content": "Content 1, testing"+'a'*30, "to_mail":"mail@mail.es", "scheduled_time":'2019-12-28T12:58:15'}))
    elements.append(json.dumps({"subject": "Subject test 2", "content": "Content 2, testing"+'a'*30, "to_mail":"mail@mail.es", "scheduled_time":'2019-12-28T12:58:15'}))
    elements.append(json.dumps({"subject": "Subject test 3", "content": "Content 3, testing"+'a'*30, "to_mail":"mail@mail.es", "scheduled_time":'2019-12-28T12:58:15'}))
    elements.append(json.dumps({"subject": "Subject test 4", "content": "Content 4, testing"+'a'*30, "to_mail":"mail@mail.es", "scheduled_time":'2019-12-28T12:58:15'}))
    elements.append(json.dumps({"subject": "Subject test 5", "content": "Content 5, testing"+'a'*30, "to_mail":"mail@mail.es", "scheduled_time":'2019-12-28T12:58:15'}))

    return elements

# Print some info
print('Sending ' + fixture + ' fixture to ' + URL + '.')

# Load right fixture
params = []
if fixture == 'events':
    params = define_events_fixture()
elif fixture == 'notifications':
    params = define_notifications_fixture()

# Send requests
try:
    for p in params:
        print("Sending request...")
        r = requests.post(url=URL, data=p)
        print('    Received response with status: ' + str(r.status_code))
except requests.exceptions.MissingSchema:
    print('Error sending requests, check that the "url" is right.')