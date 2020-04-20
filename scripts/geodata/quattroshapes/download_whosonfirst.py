import collections
import fnmatch
import json
import os
import subprocess

import pycountry


'''
alternative data source to quattroshapes as suggested by its author, as links to quattroshapes files are down
central repository: https://github.com/whosonfirst-data/whosonfirst-data/
each country's data has its own repository, this script just clones all of them
'''


if __name__ == "__main__":
    for country in pycountry.countries:
        repo = "whosonfirst-data-admin-{}".format(country.alpha2.lower())
        if not os.path.exists(os.path.join("data", "whosonfirst", repo)):
            subprocess.call(["git", "clone", "https://github.com/whosonfirst-data/{}".format(repo)])
    
    counter = collections.defaultdict(int)
    matches = []
    for root, dirnames, filenames in os.walk(os.path.join("data", "whosonfirst")):
        for filename in fnmatch.filter(filenames, "*.geojson"):
            matches.append(os.path.join(root, filename))
            # print matches[-1]
    for fname in matches:
        with open (fname) as f:
            geojson = json.load(f)
        if not geojson["properties"].get("wof:superseded_by", ""):
            counter[geojson["properties"].get("wof:placetype", "undefined")] += 1
    
    print counter 
