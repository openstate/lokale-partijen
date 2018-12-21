#!/usr/bin/env python

import sys
import os
import re
import csv
from time import sleep
import json
import configparser


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def load_party_info(config):
    data = []
    with open('data/lokaal.json') as in_file:
        data = json.load(in_file)
    return data


def main():
    config = load_config()
    parties = load_party_info(config)
    for party in parties:
        if 'website' in party['Sites']:
            print(party['Sites']['website'])
    return 0

if __name__ == '__main__':
    sys.exit(main())
