#!/usr/bin/python3
import sys
import jenkins
from firebase import firebase

JENKINS_URL = ''  # Enter Jenkins URL like http://localhost:8080
JENKINS_USERNAME = ''  # Enter available Jenkins username
JENKINS_APITOKEN = ''  # Enter Jenkins API token (or password if Jenkins < 1.5)
FIREBASE_DSN = ''  # Enter your firebase domain
FIREBASE_INVALID_CHARSET = '.$#[]/'


if __name__ == "__main__":
    build_number = int(sys.argv[1])
    job_name = sys.argv[2]

    server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_APITOKEN)
    build_info = server.get_build_info(job_name, build_number)

    firebase = firebase.FirebaseApplication(FIREBASE_DSN)

    # Remove invalid character for firebase
    firebase_job_name = job_name
    for ic in FIREBASE_INVALID_CHARSET:
        if ic in firebase_job_name:
            firebase_job_name = firebase_job_name.replace(ic, '')

    # Post new job result to firebase
    data = {'result': build_info['result'], 'timestamp': build_info['timestamp']}
    firebase.put('/job/' + firebase_job_name, build_number, data)
