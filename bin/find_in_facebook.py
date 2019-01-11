#!/usr/bin/env python

import sys
import os
import re
import csv
from time import sleep
import json
import configparser

from googleapiclient.discovery import build
import requests

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def import_results():
    result = []
    with open('data/Zetelverdeling_alle_gemeenten_GR20180321.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        # weird BOM kind of like thing
        header = [x.replace('\ufeff', '') for x in reader.__next__()]
        for row in reader:
            record = dict(zip(header, row))
            result.append(record)
    return result


def import_parties():
    result = []
    with open('data/landelijk.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # weird BOM kind of like thing
        header = [x.replace('\ufeff', '') for x in reader.__next__()]
        for row in reader:
            result += row
    return list(set([r.lower() for r in result]))


def get_local_parties_results(results, parties):
    local_parties = []
    for result in results:
        if re.sub('\s*\(.+\)$', '', result['Partij'].lower()) not in parties:
            local_parties.append(result)
    return local_parties


def normalize_party_name(full_party_name):
    parts = [x.strip() for x in full_party_name.rsplit('(', 1)]
    if len(parts) == 1:
        result = full_party_name
    else:
        if len(parts[1]) > len(parts[0]):
            result = parts[1].replace(')', '')
        else:
            result = parts[0]
    return result.lower()


def get_local_party_links(local_party, service, config):
    fb_api_version = config['facebook']['api_version']
    fb_app_id = config['facebook']['app_id']
    fb_app_secret = config['facebook']['app_secret']
    # TODO: needs to point to posts, but have feecd in the sources config. Now for a quick fix
    graph_url = "https://graph.facebook.com/%s/search?q=%s&fields=id,name,link,is_unclaimed&access_token=%s" % (
                'pages', '"%s"+"%s"' % (
                    local_party['Partij'].lower().replace(' ', '+'),
                    local_party['RegioNaam'].lower().replace(' ', '+')),
                u"%s|%s" % (fb_app_id, fb_app_secret,),)
    r = requests.get(graph_url)
    # check if we get good status codes
    if (r.status_code >= 300) or (r.status_code < 200):
        print("%s got status code: %s" % (graph_url, r.status_code,))

    results = r.json()
    if len(results['data']) > 0:
        return [(results['data'][0]['link'], 'Facebook')]
    return []


def main():
    config = load_config()
    results = import_results()
    parties = import_parties()

    all_results = []
    local_parties = get_local_parties_results(results, parties)
    service = build(
        "customsearch", "v1",
        developerKey=config['google']['dev_key'])
    for lp in local_parties[:10]:
        lp['Sites'] = {
            y: x for x, y in get_local_party_links(lp, service, config)}
        all_results.append(lp)
        sleep(1)
    print(json.dumps(all_results, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
