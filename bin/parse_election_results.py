#!/usr/bin/env python

import sys
import os
import re
import csv
from time import sleep
import json
import configparser

from googleapiclient.discovery import build


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
    try:
        search_results = service.cse().list(
            q='%s %s' % (
                normalize_party_name(local_party['Partij']),
                local_party['RegioNaam'].lower(),),
            cx=config['google']['cx']).execute()
    except Exception as e:
        search_results = {'items': []}
    results = []
    facebook_links = 0
    website_links = 0
    try:
        items = search_results['items']
    except KeyError:
        items = []

    for res in items:
        link = res['link']
        if (
            (facebook_links == 0) and
            re.search('facebook\.com\/', link) and
            not re.search('\/posts\/', link)
        ):
            results.append((link, 'facebook'))
            facebook_links += 1
        if (
            (website_links == 0) and
            re.search('\.(nl|nu|com)\/?$', link) and
            not re.search('\.facebook\.com\/', link)
        ):
            results.append((link, 'website'))
            website_links += 1
    return results


def main():
    config = load_config()
    results = import_results()
    parties = import_parties()

    all_results = []
    local_parties = get_local_parties_results(results, parties)
    service = build(
        "customsearch", "v1",
        developerKey=config['google']['dev_key'])
    for lp in local_parties:
        lp['Sites'] = {
            y: x for x, y in get_local_party_links(lp, service, config)}
        all_results.append(lp)
        sleep(1)
    print(json.dumps(all_results, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
