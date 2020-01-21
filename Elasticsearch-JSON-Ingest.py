import requests
import json
import os
from elasticsearch import Elasticsearch

# JMS
# ElasticSearch Ingest Script
# https://elasticsearch-py.readthedocs.io/en/master/api.html
#

# Statically set PCAP folder location.

print('Set JSON Ingest Directory: \n')
directory = input('')
print(f'Directory Set: {directory}')  # new string formatting
print(f'Set ElasticSearch Index Name: \n')
index_name = input('')
print(f'Index is now set to: {index_name}')

print('Checking for Elasticsearch....\n...\n...')

#
# Check Elasticsearch connectivity.
#
try:
    res = requests.get('http://127.0.0.1:9200')
    print('Connection OK.\n\n')
    # Print JSON Response from Elasticsearch with server information, including version, etc
    #
    print('Elasticsearch Server Information:\n\n {}'.format(res.content))  # Alternative string formatting.

except Exception as e:
    print('Check ElasticSearch Connection')
    print(e)

print('\nDo you want to continue?(Y/N)\n')
check_for_go = input('')    # Do you know if you wanna go?

if check_for_go.upper != 'Y':
    print('\nDid not enter "Y". Exiting.....\n')
    os.exit()

# Setup ElasticSearch.
#

es = Elasticsearch(hosts=[{'host': 'localhost', 'port': '9200'}])

# This is the JSON folder to Elasticsearch iteration.
#
idNumIter = 1

try:
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            f = open(filename)
            print('Reading JSON File Information: \n', os.fstat(f))
            packet_content = f.read()
            # Package JSON into ElasticSearch.
            es.index(index=index_name, ignore=400, doc_type='PCAP_to_JSON',
                     id=idNumIter, body=json.loads(packet_content))
            idNumIter += 1
except Exception as e:
    # Something bad happened.
    print('Halting.\n\n\n\n')
    print(e)  # print(e.message)  Exception subclasses may or may not have the message attribute
    raise

# Checking for successful index creation in Elasticsearch
#
print('Retrieving first indexed sample from uploaded JSON captures: \n')

try:
    print(es.get(id=1, index=index_name, doc_type="PCAP_to_JSON"))
except Exception as e:
    # Likely an indexing performance issue if connection error.
    # Check for index status in Kibana before running again.
    print(e)

print(f"\n\n\n{es.count(index=[index_name])}")
















