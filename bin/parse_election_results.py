#!/usr/bin/env python

import sys
import os
import re
import csv
from time import sleep
import json

from googlesearch import search


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


def get_local_party_links(local_party):
    search_results = search(
        '%s %s' % (local_party['Partij'].lower(), local_party['RegioNaam'].lower(),), stop=20)
    results = []
    for link in search_results:
        if (
            re.search('facebook\.com\/', link) and
            not re.search('\/posts\/', link)
        ):
            results.append((link, 'facebook'))
        if re.search('\.(nl|nu|com)\/?$', link):
            results.append((link, 'website'))
    return results


def main():
    results = import_results()
    parties = import_parties()

    all_results = []
    local_parties = get_local_parties_results(results, parties)
    for lp in local_parties:
        lp['Sites'] = {y: x for x, y in get_local_party_links(lp)}
        all_results.append(lp)
        sleep(1)
    print(json.dumps(all_results))
    return 0

if __name__ == '__main__':
    sys.exit(main())
