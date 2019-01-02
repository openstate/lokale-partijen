# lokale-partijen
Lokale partijen

# Usage

1. This depends on Google's Custom Search (and API). You need to [buld a custom search](https://developers.google.com/custom-search/docs/tutorial/introduction) [here](https://cse.google.com/cse/all) (Copy the search engine ID) and enable the Custom Search API in
[Cloud Developer's console](https://console.developers.google.com/apis/dashboard?project=stembureaus-197115&authuser=1&organizationId=419198286635&duration=PT1H) and copy the API Key
2. `cp config.ini.example config.ini` and edit it accordingly (`cx` is the custom search ID and `dev_key` is the developer key)
3. `docker-compose up -d`
4. `docker exec python bin/parse_election_results.py >data/lokaal.json`
5. `docker exec python bin/find_blogs.py >data/lokaal-with-feeds.json`
6. `docker exec python bin/find_content_in_feeds.py >data/lokaal-full-content.json`
