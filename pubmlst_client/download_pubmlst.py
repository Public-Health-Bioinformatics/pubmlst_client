#!/usr/bin/env python

import argparse
import json
import os
import re
import urllib.request
import sys
import time
import datetime

from pubmlst_client.util import get


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", "-o", dest="outdir", default='./mlstdb', help="output directory")
    parser.add_argument("--base-url", "-b", dest="base_url", default='http://rest.pubmlst.org/db', help="Base URL for the API. Suggested values are: http://rest.pubmlst.org/db (default), https://bigsdb.pasteur.fr/api/db")
    args = parser.parse_args()

    api_url_base = args.base_url

    url_base_response = json.loads(get(api_url_base))

    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    for db in url_base_response:
        databases =  db['databases']
        for database in databases:
            if '_seqdef' in database['name']:
                db_download_path_1 = '%s/%s' % (args.outdir,database['name'][8:-7])
                # Find MLST Schemes
                schemes = json.loads(get(''.join([database['href'],'/schemes'])))
                mlst_schemes = []
                for scheme in schemes['schemes']:
                    if 'MLST' in scheme['description'] and 'cgMLST' not in scheme['description'] and 'eMLST' not in scheme['description'] :
                        mlst_schemes.append(scheme['scheme'].split('/')[-1])
                mlst_schemes.sort()
                for i in range(len(mlst_schemes)):
                    if i > 0:
                        db_download_path = db_download_path_1 + "_%s" % (i+1)
                        os.mkdir(db_download_path)
                    else:
                        db_download_path = db_download_path_1
                        os.mkdir(db_download_path)
                    plaintext_header = {'Content-Type': 'text/plain'}
                    types_tsv = get(''.join([database['href'],'/schemes/%s/profiles_csv' % mlst_schemes[i]]), headers=plaintext_header).decode('utf-8')
                    if i > 0:
                        output_filename = os.path.join( db_download_path , database['name'][8:-7] + '_%s'% (i+1) +'.txt')
                    else:
                        output_filename = os.path.join( db_download_path , database['name'][8:-7] + '.txt')
                    with open(output_filename, 'w') as f:
                        f.write(types_tsv)
                    log_msg = {
                            'timestamp': str(datetime.datetime.now().isoformat()),
                            'event': 'file_downloaded',
                            'filename': output_filename,
                        }
                    print(json.dumps(log_msg), file=sys.stderr)
                    db_res = json.loads(get(''.join([database['href'],'/schemes/%s' % mlst_schemes[i]])))
                    for locus_url in db_res['loci']:
                        locus = json.loads(get(locus_url))
                        alleles_fasta = get(locus['alleles_fasta'], headers=plaintext_header).decode('utf-8')
                        output_filename = os.path.join(db_download_path, locus['id'] + '.fasta')
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
