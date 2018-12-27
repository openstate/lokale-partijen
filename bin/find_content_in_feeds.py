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
import feedparser
from bs4 import BeautifulSoup


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def load_party_info(config):
    data = []
    with open('data/lokaal-with-feeds.json') as in_file:
        data = json.load(in_file)
    return data


def get_feed_info(party, config):
    result = deepcopy(party)
    try:
        feed = feedparser.parse(party['feed'])
    except Exception as e:
        feed = None

    if feed is None:
        return

    if len(feed.entries) > 0:
        avg_len = (sum(
            [len(x.description) for x in feed.entries]) / len(feed.entries))
    else:
        avg_len = 141  # assume?

    result['full_content'] = (avg_len > 140)

    return result


def main():
    config = load_config()
    parties = load_party_info(config)
    parties_with_blogs = []
    for party in parties:
        if 'feed' in party and party['feed'] is not None:
            sys.stderr.write("%s\n" % (party['feed']))
            res = get_feed_info(party, config)
            if res is not None:
                parties_with_blogs.append(res)
    print(json.dumps(parties_with_blogs, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
