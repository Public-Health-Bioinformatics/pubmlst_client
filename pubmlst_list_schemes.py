#!/usr/bin/env python

import argparse
import json
import os
import re
import requests
import time
from pprint import pprint

def plaintext_parser(response_content):
    return response_content

def get(api_url, headers={'Content-Type': 'application/json'}, parser=json.loads):
    time.sleep(1) # give the api a rest
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return parser(response.content.decode('utf-8'))
    else:
        return None

def main(args):
    print('\t'.join(['db_name', 'scheme', 'scheme_type'])) 
    api_url_base = 'http://rest.pubmlst.org/db'

    url_base_response = get(api_url_base)
    for db in url_base_response:
        name = db['name']
        databases =  db['databases']
        for database in databases:
            # if True:
            organism_match = re.search('pubmlst_(.+)_seqdef$', database['href'])
            if organism_match:
                organism = organism_match.group(1)
                seqdef = get(database['href'])
                if seqdef['schemes']:
                    schemes = get(seqdef['schemes'])
                    for scheme in schemes['schemes']:
                        description = scheme['description']
                        print('\t'.join([name, organism, description]))

            
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    main(args)
