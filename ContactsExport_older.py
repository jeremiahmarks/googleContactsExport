# Rewrite to pull all contacts, create a list of their ids
# cycle through ids
# @Author: jeremiah.marks
# @Date:   2016-04-07 13:51:32
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2016-04-07 20:11:43
import logging
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
APPLICATION_NAME = 'contactsexportforinfusionsoft'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
  print "about to get contacts"
  if nextPageToken is None:
    return service.people().connections().list(resourceName='people/me', pageSize=50).execute()
  else:
    return service.people().connections().list(resourceName='people/me', pageSize=50, pageToken=nextPageToken).execute()

allcontacts={}
def thatMainScript():
  global service
  global allcontacts
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('people', 'v1', http=http,
      discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
  # allcontacts={}
  nextpagetoken = None
  print "Retrieving all contacts"
  while True:
    # print "sleeping 10"
    # time.sleep(10)
    print "total contacts: " + str(len(allcontacts))
    results = getContacts(nextpagetoken)
    connections = results.get('connections', [])
    print "doing a getBatch"
    contacts=service.people().getBatchGet(resourceNames=[ec['resourceName'] for ec in connections]).execute()
    for eachcon in contacts['responses']:
        allcontacts[eachcon['requestedResourceName']]=eachcon
    if 'nextPageToken' not in results:
      return allcontacts
    nextpagetoken = results['nextPageToken']

def getInnerCols(columnName, columnData):
    returnDict={}
    if isinstance(columnData, list):
        for position, item in enumerate(columnData):
            colnam = columnName+str(position)
            returnDict.update(getInnerCols(colnam, item))
    elif isinstance(columnData, dict):
        for eachkey in columnData:
            colnam = columnName+":"+str(eachkey)
            returnDict.update(getInnerCols(colnam, columnData[eachkey]))
    else:
        returnDict[columnName] = str(columnData)
    return returnDict

def gatherneededcolumns(ratherLargeDict):
    newfile=[]
    columns=set()
    for eachUserId in ratherLargeDict:
        newContactRow={}
        thiscontact=ratherLargeDict[eachUserId]['person']
        for eachcolumn in thiscontact:
            newContactRow.update(getInnerCols(eachcolumn, thiscontact[eachcolumn]))
        newfile.append(newContactRow)
        columns.update(newContactRow.keys())
    newfile = ensureallrowshaveallcols(newfile, columns)
    return newfile

def ensureallrowshaveallcols(thenewfile, thecols):
    for eachrow in thenewfile:
        for eachkey in thecols:
            if eachkey not in eachrow:
                eachrow[eachkey]=''
    return thenewfile
