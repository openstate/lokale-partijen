#!/usr/bin/env python

import sys
import os
import re
import csv
import codecs


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

def main():
    results = import_results()
    parties = import_parties()
    for result in results:
        if re.sub('\s*\(.+\)$', '', result['Partij'].lower()) not in parties:
            print(result)
    return 0

if __name__ == '__main__':
    sys.exit(main())
