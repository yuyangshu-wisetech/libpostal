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
        if not os.path.exists(repo):
            try:
                subprocess.call(["git", "clone", "https://github.com/whosonfirst-data/{}".format(repo)])
            except:
                print "no data for {}".format(repo[:-2])
