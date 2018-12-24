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


def _find_blogging_engine(url, soup):
    elem = soup.find('meta', {'name': 'generator'})
    if elem is not None:
        try:
            engine = elem['content'].split()[0]
        except Exception:
            engine = None
        return engine.lower()


def _find_blogging_feed(url, soup):
    elem = soup.find('link', {'rel': 'alternate', 'type': "application/rss+xml" })
    if elem is not None:
        return urljoin(url, elem['href'])


def get_blog_info(party, config):
    result = deepcopy(party)
    try:
        resp = requests.get(party['Sites']['website'])
    except Exception as e:
        resp = None

    if resp is None:
        return

    if resp.status_code >= 200 and resp.status_code < 300:
        soup = BeautifulSoup(resp.content, 'html.parser')
        result['engine'] = _find_blogging_engine(resp.url, soup)
        result['feed'] = _find_blogging_feed(resp.url, soup)
    return result


def main():
    config = load_config()
    parties = load_party_info(config)
    parties_with_blogs = []
    for party in parties:
        if 'website' in party['Sites']:
            res = get_blog_info(party, config)
            if res is not None:
                parties_with_blogs.append(res)
    print(json.dumps(parties_with_blogs, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
