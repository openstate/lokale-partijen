#!/usr/bin/env python

import sys
import os
import re
import csv
from time import sleep
import json
import configparser
from copy import deepcopy
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def load_party_info(config):
    data = []
    with open('data/lokaal.json') as in_file:
        data = json.load(in_file)
    return data


def get_party_name_parts(full_party_name, region):
    parts = [x.strip() for x in full_party_name.rsplit('(', 1)]
    if len(parts) == 1:
        result = re.split('(\s+|\-|/|\.)', full_party_name)
    else:
        result = re.split('(\s+|\-|/|\.)', parts[0]) + re.split('(\s+|\-|/|\.)', parts[1].replace(')', ''))
    result += re.split('(\s+|\-|/|\.)', region)
    better = [re.sub('(\.|\s*)', '', x).strip().lower() for x in result]
    return [x for x in better if re.sub('(\s+|\-|/|\.)', '', x).strip() != '']


def count_parts_present(parts, website):
    num_parts = 0
    for part in parts:
        if part in website:
            num_parts += 1
    return num_parts


def check_if_suspicious(party, config):
    parts = get_party_name_parts(party['Partij'], party['RegioNaam'])
    num_match = count_parts_present(parts, party['Sites']['website'])
    if num_match < 1:
        sys.stderr.write("%s -> [%s] <=> %s : %s\n" % (
            party['Partij'], ' '.join(parts), party['Sites']['website'],
            num_match))
    return


def main():
    config = load_config()
    parties = load_party_info(config)
    parties_with_blogs = []
    for party in parties:
        if 'website' in party['Sites']:
            res = check_if_suspicious(party, config)
            if res is not None:
                parties_with_blogs.append(res)
    print(json.dumps(parties_with_blogs, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
