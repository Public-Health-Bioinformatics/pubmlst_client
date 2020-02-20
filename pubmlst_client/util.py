import datetime
import json
import sys
import time
import urllib.request


def get(api_url, headers={'Content-Type': 'application/json'}, max_retries=5):
    response = None
    retries = 0
    request = urllib.request.Request(api_url, headers=headers)
    while retries < max_retries:
        time.sleep(1) # give the api a rest
        try:
            with urllib.request.urlopen(request) as response:
                response_content = response.read()
                if response.status == 200:
                    retries = 0
                    break
        except:
            log_msg = {
                'timestamp': str(datetime.datetime.now().isoformat()),
                'event': 'connection_error',
                'url': api_url,
                'retries': retries,
            }
            print(json.dumps(log_msg), file=sys.stderr)
            retries += 1

    if response and response.status == 200:
        return response_content
    elif response and response.status == 401:
        log_msg = {
                'timestamp': str(datetime.datetime.now().isoformat()),
                'event': 'connection_error',
                'url': api_url,
                'message': 'Unauthorized',
            }
        print(json.dumps(log_msg), file=sys.stderr)
        return None
    else:
        if retries == max_retries:
            log_msg = {
                'timestamp': str(datetime.datetime.now().isoformat()),
                'event': 'max_retries',
                'url': api_url,
            }
            print(json.dumps(log_msg), file=sys.stderr)
        return None
