#!/usr/bin/env python

import argparse
import datetime
import json
import os
import sys
import time

from pubmlst_client.util import get


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--scheme_name", "-s", dest="scheme_name", help="scheme name", required=True)
    parser.add_argument("--scheme_id", "-i", dest="scheme_id", default="1", help="scheme id")
    parser.add_argument("--outdir", "-o", dest="outdir", default='.', help="output directory")
    parser.add_argument("--base-url", "-b", dest="base_url", default='http://rest.pubmlst.org/db', help="Base URL for the API. Suggested values are: http://rest.pubmlst.org/db (default), https://bigsdb.pasteur.fr/api/db")
    args = parser.parse_args()
    
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    api_url_base = args.base_url

    scheme_url = '/'.join([
        api_url_base,
        'pubmlst_' + args.scheme_name + '_seqdef',
        'schemes',
        args.scheme_id
    ])

    scheme_response = json.loads(get(scheme_url))
    
    for locus_url in scheme_response['loci']:
        locus = json.loads(get(locus_url))
        plaintext_header = {'Content-Type': 'text/plain'}
        alleles_fasta = get(locus['alleles_fasta'], headers=plaintext_header).decode('utf-8')
        output_filename = os.path.join(args.outdir, locus['id'] + '.fasta')
        with open(output_filename, 'w') as f:
            f.write(alleles_fasta)
        log_msg = {
            'timestamp': str(datetime.datetime.now().isoformat()),
            'event': 'file_downloaded',
            'filename': output_filename,
        }
        print(json.dumps(log_msg), file=sys.stderr)
            
        

if __name__ == '__main__':    
    main()
