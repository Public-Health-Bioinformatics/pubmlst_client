#!/usr/bin/env python

import argparse
import json
import os
import requests
import time
from pprint import pprint

def plaintext_parser(response_content):
    return response_content

def get(api_url, headers={'Content-Type': 'application/json'}, parser=json.loads):
    retries = 0
    while retries < 5:
        try:
            response = requests.get(api_url, headers=headers)
            retries = 0
            break
        except requests.exceptions.ConnectionError as e:
            log_msg = {
                'event': 'connection_error',
                'url': api_url,
                'retries': retries,
            }
            print(json.dumps(log_msg))
            retries += 1
            
    if response.status_code == 200:
        return parser(response.content.decode('utf-8'))
    else:
        return None

def main(args):

    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    api_url_base = 'http://rest.pubmlst.org/db'

    schemes_url = '/'.join([
        api_url_base,
        'pubmlst_' + args.scheme + '_seqdef',
        'schemes'
    ])

    schemes_response = get(schemes_url)
    scheme_url = list(filter(lambda scheme: scheme['description'] == args.scheme_type, schemes_response['schemes']))[0]['scheme']

    scheme_response = get(scheme_url)
    
    for locus_url in scheme_response['loci']:
        locus = get(locus_url)
        plaintext_header = {'Content-Type': 'text/plain'}
        alleles_fasta = get(locus['alleles_fasta'], plaintext_header, plaintext_parser)
        output_filename = os.path.join(args.outdir, locus['id'] + '.fasta')
        with open(output_filename, 'w') as f:
            f.write(alleles_fasta)
        log_msg = {
            'event': 'file_downloaded',
            'filename': output_filename,
        }
        print(json.dumps(log_msg))
            
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheme", "-s", dest="scheme", help="scheme to download")
    parser.add_argument("--scheme_type", "-t", dest="scheme_type", default="cgMLST", help="Type of scheme to download ('cgMLST', 'MLST')")
    parser.add_argument("--outdir", "-o", dest="outdir", default='.', help="output directory")
    args = parser.parse_args()
    
    main(args)
