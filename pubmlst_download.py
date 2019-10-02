#!/usr/bin/env python

import argparse
import json
import os
import requests
from pprint import pprint

def plaintext_parser(response_content):
    return response_content

def get(api_url, headers={'Content-Type': 'application/json'}, parser=json.loads):
    response = requests.get(api_url, headers=headers)

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
        with open(os.path.join(args.outdir, locus['id'] + '.fasta'), 'w') as f:
            f.write(alleles_fasta)
            
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheme", "-s", dest="scheme", help="scheme to download")
    parser.add_argument("--scheme_type", "-t", dest="scheme_type", default="cgMLST", help="Type of scheme to download ('cgMLST', 'MLST')")
    parser.add_argument("--outdir", "-o", dest="outdir", default='.', help="output directory")
    args = parser.parse_args()
    
    main(args)
