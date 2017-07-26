import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory

from datetime import datetime
from mechanize import Browser

import re
import datetime

import boto3
import dropbox

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

@app.route('/')
def index():
    return "what are you looking? probably its not here!"



@app.route("/dailyreport")
def test():
    # creating a temp file from the report
    tempfile = 'temp.txt'
    file = open(path+tempfile,'w')

    file.write(fetch_sf_report(os.environ['sf_report_id']))
    file.close()
    # creating daily filename
    filename = 'SDE_Backlog_'+datetime.date.today().strftime('%m-%d-%Y')+'.csv'

    # invoking functions and executing
    create_csv_from_txt(filename)
    #send_mail(path+filename)

        # Configuration for AWS
        #bucket = 'enriquemanuel-work'
        #s3_upload(filename,path+filename, bucket )

    # configuration for Dropbox
    dropbox_upload(path,filename)

    os.remove(path+filename)
    content = {'information': 'email sent.'}
    return 'Message sent at  %s' % datetime.date.today().strftime('%m-%d-%Y')



path = os.environ['OPENSHIFT_TMP_DIR']
#path = os.getcwd()

def fetch_sf_report(report_id):
    login_uri = "https://login.salesforce.com/"
    username = os.environ['evalenzuela_username']
    password = os.environ['evalenzuela_password']
    b = Browser()
    b.set_handle_robots(False)
    b.open(login_uri + '/?un=' + username + '&pw=' + password + '&startURL=' + report_id + '?export=1&enc=UTF-8&xf=csv')
    link = b.find_link(url_regex=re.compile("^https://[^/]*salesforce.com/" + report_id))
    return b.follow_link(link).read()

def send_mail_error(msg):
    import requests
    requests.packages.urllib3.disable_warnings()
    # send mail via mailgun
    requests.post(os.environ['mailgun_domain_endpoint'],
        auth=("api",os.environ['MAILGUN_API_KEY']),
        files=[("attachment", open(filename))],
        data={"from":os.environ['from_email'],
        "to":os.environ['from_email'],
        "subject": "SDE Backlog - "+datetime.date.today().strftime('%m-%d-%Y'),
        "text": "Daily report by evalenzuela had an error. Error below \n"+msg })

def send_mail(filename):
    import requests
    requests.packages.urllib3.disable_warnings()
    # send mail via mailgun
    requests.post(os.environ['mailgun_domain_endpoint'],
        auth=("api",os.environ['MAILGUN_API_KEY']),
        files=[("attachment", open(filename))],
        data={"from":"os.environ['from_email'],
        "to":os.environ['from_email'],
        "subject": "SDE Backlog - "+datetime.date.today().strftime('%m-%d-%Y'),
        "text": "Daily report by evalenzuela" })


def create_csv_from_txt(filename):
    # creating the final csv file
    import csv
    with open(path+filename, 'wb') as f:
        writer = csv.writer(f)
        tempfile = path+'temp.txt'
        with open(tempfile, 'rb') as csvfile:
            rows = csv.reader(csvfile)
            writer.writerows(rows)
    # erase the temp file
    import os
    os.remove(path+'temp.txt')

def dropbox_upload(path, filename):
    import dropbox
    key=os.environ['DROPBOX_CLIENT_API_KEY']
    client = dropbox.client.DropboxClient(os.environ['DROPBOX_CLIENT_API_KEY'])
    f = open(path+filename, 'rb')
    response = client.put_file(filename, f)


def s3_upload(filename,pathandfile, bucket):

    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
    s3.upload_file(pathandfile,bucket,filename)


if __name__ == '__main__':
    app.run()
