#!/usr/bin/env python

import argparse
import json
import re

from typing import Union

from pubmlst_client.util import get


def get_bigsdb_schemes(url_base_response: list[dict],
                       details_fields,
                       pattern: Union[str, None] = None,
                       exclude_pattern: Union[str, None] = None, 
                       names_only: bool = False) -> list[str]:
    
    scheme_list = []
    for db in url_base_response:
        databases =  db['databases']
        for database in databases:
            if exclude_pattern != "":
                if re.search('pubmlst_(' + '.*' + exclude_pattern + '.*' + ')_seqdef$', database['name']):
                    continue
            scheme_match = re.search('pubmlst_(' + '.*' + pattern + '.*' + ')_seqdef$', database['name'])
            if scheme_match:
                scheme_name = scheme_match.group(1)
                if names_only:
                    scheme_list.append(scheme_name)
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
                                scheme_list.append('\t'.join(map(str, [scheme_name] + list(details.values()))))
        return scheme_list


def get_cgmlst_schemes(url_base_response: list[dict],
                       pattern: Union[str, None] = None,
                       exclude_pattern: Union[str, None] = None,
                       names_only: bool = False) -> list[str]:

    scheme_list = []
    for index, scheme in enumerate(url_base_response):
        if exclude_pattern != "":
            if re.search(exclude_pattern, scheme['Scheme'], re.IGNORECASE):
                continue
        scheme_match = re.search(pattern, scheme['Scheme'])
        if scheme_match:
            scheme_name = scheme['Scheme']
            if names_only:
                print(scheme_name)
                continue
# name    id      description     locus_count     records last_added      last_updated
            scheme_details = {}
            scheme_details['id'] = index
            scheme_details['locus_count'] = scheme['Target Count']
            scheme_details['records'] = 'UNKNOWN'
            scheme_def_response = get(scheme['Scheme Href'])
            if scheme_def_response:
                scheme_def = json.loads(scheme_def_response)
                last_updated_match = re.search(r'\([^;]+, (\d+-\w+-\d+).*\)', scheme_def['Seed Genome'])
                if last_updated_match:
                    scheme_details['last_added'] = last_updated_match.group(1)
                else:
                    scheme_details['last_added'] = 'UNKNOWN'
                scheme_details['last_updated'] = scheme_def.get('Last Change', 'UNKNOWN')
            scheme_list.append('\t'.join(map(str, [scheme_name] + list(scheme_details.values()))))

    return scheme_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pattern', '-p', default="", help="regex pattern to filter scheme names")
    parser.add_argument('--exclude_pattern', '-e', default="", help="regex pattern to filter scheme names")
    parser.add_argument('--names_only', '-n', default="", action='store_true', help="Only show scheme names")
    parser.add_argument("--base-url", "-b", dest="base_url", default='http://rest.pubmlst.org/db', help="Base URL for the API. Suggested values are: http://rest.pubmlst.org/db (default), https://bigsdb.pasteur.fr/api/db or https://cgmlst.org/ncs/api (using cgmlstorg api type)")
    parser.add_argument('--api-type', default='bigsdb', choices=['bigsdb', 'cgmlstorg'], help="API to use. Suggested values are: bigsdb (default), cgmlstorg")

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
    api_type = args.api_type

    url_base_response = json.loads(get(api_url_base))

    if api_type == 'bigsdb':
        schemes = get_bigsdb_schemes(url_base_response, details_fields, args.pattern, args.exclude_pattern, args.names_only)
    else:
        schemes = get_cgmlst_schemes(url_base_response, args.pattern, args.exclude_pattern, args.names_only)

    for scheme_info in schemes:
        print(scheme_info)

if __name__ == '__main__':
    main()
