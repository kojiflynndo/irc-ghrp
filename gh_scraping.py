'''
File for scraping GitHub historical commits from @markbrough's repository
containing COVID-19 GHRP data
Saves the list of SHAs in order from least to most recent as a pickle

Last change: 30 December 2020
'''

import requests
import json
import pandas as pd
import pickle
import os

def scrape():
    COMMITS_URL = "https://api.github.com/repos/markbrough/covid19-data/commits?path=fts-emergency-911.json&sha=gh-pages&page={}"

    page = 0
    commits = []
    while True:
        req = requests.get(COMMITS_URL.format(page), auth=('kojiflynndo', '6d945260869090d6ce8c074a43467ea5366ddec6')).json()
        if req == []: break
        page += 1
        commits += list(map(lambda commit : commit['sha'], req))
    commits.reverse()

    f_loc = os.getcwd() + '/output/gh_sha.txt'
    with open(f_loc, 'wb') as fp:
        pickle.dump(commits, fp)

    print('Done pickling, file available at', f_loc)
