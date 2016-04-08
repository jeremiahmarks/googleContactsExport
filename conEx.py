# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2016-04-08 06:31:19
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2016-04-08 08:15:37
import logging
import httplib2
import time
import os
import csv

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import argparse

flags = argparse.Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR', noauth_local_webserver=True)
# SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
SCOPES = 'https://www.googleapis.com/auth/contacts'
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

def getContacts():
    global service
    servicecalls=0
    #Only pulling five to test the pagination part of things
    templist=[]
    contactGetter = lambda x: service.people().connections().list(resourceName='people/me', pageSize=500, pageToken=x).execute()
    thesecontacts = contactGetter(None)
    servicecalls+=1
    templist.append(thesecontacts[u'connections'])
    while 'nextPageToken' in thesecontacts:
        print servicecalls
        print "doing an inside"
        thesecontacts = contactGetter(thesecontacts['nextPageToken'])
        servicecalls+=1
        templist.append(thesecontacts[u'connections'])
    allcontacts=[]
    for eachcall in templist:
        for eachcontact in eachcall:
            allcontacts.append(eachcontact[u'resourceName'])
    groupedForLookup = [allcontacts[x:x+45] for x in xrange(0, len(allcontacts), 45)]
    allcon={}
    print "Total groups" + str(len(groupedForLookup))
    for eachgroup in groupedForLookup:
        try:
            contacts=service.people().getBatchGet(resourceNames=[ec for ec in eachgroup]).execute()
        except Exception, e:
            print e
            print "Crud, hit API limit, sleeping 100 seconds"
            for x in range(10):
                print "slept: " + str(x*10)
                time.sleep(10)
            contacts=service.people().getBatchGet(resourceNames=[ec for ec in eachgroup]).execute()
        for eachcon in contacts['responses']:
            if eachcon['requestedResourceName'] not in allcon:
                allcon[eachcon['requestedResourceName']]={}
            allcon[eachcon['requestedResourceName']].update(eachcon)
    return allcon

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

def ensureallrowshaveallcols(thenewfile, thecols):
    for eachrow in thenewfile:
        for eachkey in thecols:
            if eachkey not in eachrow:
                eachrow[eachkey]=''
    return thenewfile

def main():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'GoogleExport')
    global service
    global allcontacts
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('people', 'v1', http=http,
      discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
    ac=getContacts()
    templist=[]
    columns=set()
    for eachid in ac:
        newcontactrow={}
        thiscontact=ac[eachid]['person']
        for eachcol in thiscontact:
            newcontactrow.update(getInnerCols(eachcol, thiscontact[eachcol]))
        templist.append(newcontactrow)
        columns.update(newcontactrow.keys())
    newfile = ensureallrowshaveallcols(templist, columns)
    expath=os.path.join(credential_dir, 'export.csv')
    with open(expath, 'wb') as outfile:
        thiswriter = csv.DictWriter(outfile, list(columns))
        thiswriter.writeheader()
        thiswriter.writerows(newfile)
    print expath
