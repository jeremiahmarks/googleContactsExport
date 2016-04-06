# @Author: jeremiah.marks
# @Date:   2016-04-06 01:58:26
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2016-04-06 01:58:39
# @Author: jeremiah.marks
# @Date:   2016-04-06 01:21:17
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2016-04-06 01:23:21
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import argparse
flags = argparse.Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR', noauth_local_webserver=False)
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
CLIENT_SECRET_FILE = "C:\\Users\\jeremiah.marks\\Documents\\GitHub\\gdata-python-client\\client_secret.json"
APPLICATION_NAME = 'ContactsToCSV'
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
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('people', 'v1', http=http,
    discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
allcontacts={}
results = service.people().connections().list(resourceName='people/me', pageSize=10).execute()
connections = results.get('connections', [])
connections[0]
connections[0][u'resourceName']
results
results = service.people().connections().list(resourceName='people/me', pageSize=1).execute()
connections = results.get('connections', [])
connections
results
connections = results.get('connections')
connections
results = service.people().connections().list(resourceName='people/me').execute()
connections = results.get('connections')
connections[0]
def getContacts(nextPageToken=None):
  if nextPageToken is None:
    return service.people().connections().list(resourceName='people/me').execute()
  else:
    return service.people().connections().list(resourceName='people/me', nextPageToken=nextPageToken).execute()
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('people', 'v1', http=http,
    discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
allcontacts={}
nextpagetoken = None
print "Retrieving all contacts"
while True:
  print "total contacts: " + len(allcontacts)
  results = getContacts(nextpagetoken)
  connections = results.get('connections', [])
  for eachcon in connections:
    allcontacts[eachcon['resourceName']] = dict(eachcon)
  if 'nextPageToken' not in results:
    break
  nextpagetoken = results['nextPageToken']
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
print str(flags)
"""


Provides information about a list of specific people by specifying a list of requested resource names. Use people/me to indicate the authenticated user.

HTTP request

GET https://people.googleapis.com/v1/people:batchGet

Query parameters

Parameter name  Type  Description
resourceNames string  The resource name, such as one returned by people.connections.list, of one of the people to provide information about. You can include this parameter up to 50 times in one request.

"""
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
CLIENT_SECRET_FILE = "C:\\Users\\jeremiah.marks\\Documents\\GitHub\\gdata-python-client\\client_secret.json"
APPLICATION_NAME = 'ContactsToCSV'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
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
  if nextPageToken is None:
    return service.people().connections().list(resourceName='people/me').execute()
  else:
    return service.people().connections().list(resourceName='people/me', nextPageToken=nextPageToken).execute()

def main():
    """Shows basic usage of the Google People API.

    Creates a Google People API service object and outputs the name if
    available of 10 connections.
    """
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
  for eachcon in connections:
    allcontacts[eachcon['resourceName']] = dict(eachcon)
  if 'nextPageToken' not in results:
    break
  nextpagetoken = results['nextPageToken']


if __name__ == '__main__':
    main()
def getContacts(nextPageToken=None):
  if nextPageToken is None:
    return service.people().connections().list(resourceName='people/me').execute()
  else:
    return service.people().connections().list(resourceName='people/me', pageToken=nextPageToken).execute()
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
  for eachcon in connections:
    allcontacts[eachcon['resourceName']] = dict(eachcon)
  if 'nextPageToken' not in results:
    break
  nextpagetoken = results['nextPageToken']


if __name__ == '__main__':
    main()
allcontacts
nextpagetoken = None
results = getContacts(nextpagetoken)
results
connections = results.get('connections', [])
connections
def getContacts(nextPageToken=None):
  if nextPageToken is None:
    retval = service.people().connections().list(resourceName='people/me').execute()

  else:
    retval =  service.people().connections().list(resourceName='people/me', pageToken=nextPageToken).execute()
  return retval
results = getContacts(nextpagetoken)
connections = results.get('connections', [])
connections
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
  for eachcon in connections:
    allcontacts[eachcon['resourceName']] = dict(eachcon)
  if 'nextPageToken' not in results:
    break
  nextpagetoken = results['nextPageToken']
allcontacts[u'people/100239705038582327542']
