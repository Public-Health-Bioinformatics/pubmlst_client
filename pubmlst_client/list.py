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

    api_url_base = 'http://rest.pubmlst.org/db'

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
                seqdef = json.loads(get(database['href']))
                if seqdef:
                    schemes = json.loads(get(seqdef['schemes']))
                    for scheme in schemes['schemes']:
                        scheme_details = json.loads(get(scheme['scheme']))
                        if scheme_details:
                            details = {}
                            for field in details_fields:
                                try:
                                    details[field] = scheme_details[field]
                                except KeyError:
                                    details[field] = None
                            print('\t'.join(map(str, [scheme_name] + list(details.values()))), flush=True)


if __name__ == '__main__':
    main()
