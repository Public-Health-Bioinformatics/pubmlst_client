#!/usr/bin/env python

import argparse
import json
import os
import re
import urllib.request
import sys
import time

from pubmlst_client.util import get


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pattern', '-p', default="", help="regex pattern to filter scheme names")
    parser.add_argument('--exclude_pattern', '-e', default="", help="regex pattern to filter scheme names")
    parser.add_argument('--names_only', '-n', default="", action='store_true', help="Only show scheme names")
    parser.add_argument("--base-url", "-b", dest="base_url", default='http://rest.pubmlst.org/db', help="Base URL for the API. Suggested values are: http://rest.pubmlst.org/db (default), https://bigsdb.pasteur.fr/api/db")
    
    args = parser.parse_args()

    details_fields = [
        'id',
        'description',
        'locus_count',
        'records',
        'last_added',
        'last_updated',
    ]
    
    if args.names_only:
        print('name')
    else:
        print('\t'.join(['name'] + details_fields)) 

    api_url_base = args.base_url

    url_base_response = json.loads(get(api_url_base))


    for db in url_base_response:
        databases =  db['databases']
        for database in databases:
            if args.exclude_pattern != "":
                if re.search('pubmlst_(' + '.*' + args.exclude_pattern + '.*' + ')_seqdef$', database['name']):
                    continue
            scheme_match = re.search('pubmlst_(' + '.*' + args.pattern + '.*' + ')_seqdef$', database['name'])
            if scheme_match:
                scheme_name = scheme_match.group(1)
                if args.names_only:
                    print(scheme_name)
                    break
                seqdef_response = get(database['href'])
                if seqdef_response:
                    schemes_response = get(json.loads(seqdef_response)['schemes'])
                    if schemes_response:
                        for scheme in json.loads(schemes_response)['schemes']:
                            scheme_details_response = get(scheme['scheme'])
                            if scheme_details_response:
                                details = {}
                                for field in details_fields:
                                    try:
                                        details[field] = json.loads(scheme_details_response)[field]
                                    except KeyError:
                                        details[field] = None
                                print('\t'.join(map(str, [scheme_name] + list(details.values()))), flush=True)


if __name__ == '__main__':
    main()
