import fnmatch
import os
import pycountry
import requests
import subprocess
import sys
import ujson as json

this_dir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.realpath(os.path.join(os.pardir, os.pardir)))


WOF_DATA_ADMIN_REPO_URL_PREFIX = "https://github.com/whosonfirst-data/whosonfirst-data/"
WOF_DATA_ADMIN_REPO_PREFIX = "whosonfirst-data-admin-"


def clone_repo(wof_dir, repo_name):
    subprocess.call(["git", "clone", WOF_DATA_ADMIN_REPO_URL_PREFIX + repo_name])


def download_wof_data_admin(wof_dir):
    for country_object in pycountry.countries:
        repo_name = WOF_DATA_ADMIN_REPO_PREFIX + country_object.alpha2.lower()
        repo_location = os.path.join(wof_dir, repo_name)
        if not os.path.exists(repo_location):
            clone_repo(wof_dir, repo_name)


def extract_neighbourhood(wof_dir):
    neighbourhood_entries = []
    for root, dirnames, filenames in os.walk(wof_dir):
        for fname in fnmatch.filter(filenames, "*.geojson"):
            with open(os.path.join(root, fname)) as f:
                geojson = json.load(f)
                if not geojson["properties"].get("wof:superseded_by") and counter[geojson["properties"].get("wof:placetype") == "neighbourhood":
                    neighbourhood_entries.append(geojson["geometry"])

    with open(os.path.join(wof_dir, "wof_neighbourhoods.dump")) as f:
        json.dumps(neighbourhood_entries, f)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: python download_wof_postal_codes.py wof_base_dir')

    download_wof_data_admin(sys.argv[1])
    extract_neighbourhood(sys.argv[1])
