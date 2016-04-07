# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2016-04-07 13:51:32
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2016-04-07 14:41:49
import httplib2
import time
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import argparse

flags = argparse.Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR', noauth_local_webserver=True)
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
CLIENT_SECRET_FILE = "C:\\Users\\jeremiah.marks\\Documents\\GitHub\\bexport\\client_secret.json"
APPLICATION_NAME = 'ContactsToCSV'
C:\Users\jeremiah.marks\Documents\GitHub\bexport\client_secret.json
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'GoogleExport')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'GoogContactsExportToCSV')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def getContacts(nextPageToken=None):
  global service
  if nextPageToken is None:
    return service.people().connections().list(resourceName='people/me').execute()
  else:
    return service.people().connections().list(resourceName='people/me', pageToken=nextPageToken).execute()

def thatMainScript():
  global service
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('people', 'v1', http=http,
      discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
  allcontacts={}
  nextpagetoken = None
  print "Retrieving all contacts"
  while True:
    print "total contacts: " + str(len(allcontacts))
    results = getContacts(nextpagetoken)
    connections = results.get('connections', [])
    print connections
    for eachcon in connections:
        time.sleep(0.6)
        try:
          k=service.people().get(resourceName=eachcon['resourceName']).execute()
          print k
          allcontacts[eachcon['resourceName']] = k
        except Exception, e:
            print "did not get "+ eachcon['resourceName']
            print e

    if 'nextPageToken' not in results:
      break
    nextpagetoken = results['nextPageToken']
  return allcontacts
