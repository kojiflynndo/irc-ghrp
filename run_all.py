'''
'''
import pandas as pd
import numpy as np
import datetime as dt
import os
import altair as alt
import openpyxl
import toolz

from gh_scraping import scrape
from gh_processing import process
from fts_analysis import updatedFlows

from ghrp_tracker import *
from ghrp_viz import *

# flow updates and speed
def flowUpdate():
    print('scraping JSON files')
    scrape()
    print('processing JSON files')
    process()
    print('putting flow updates into csv')
    updatedFlows()

# covid cases
def covidCases():
    print('getting COVID cases from OWID')
    cumulativeCovidCases()
    covidStats()

# GHRP financing
def GHRPFinancing():
    dfGHRP = pd.read_excel(os.getcwd()+ '/input/contributions.xlsx', engine='openpyxl')
    dfGHRP = cleandf(dfGHRP)
    allFunders = getFunders(dfGHRP)
    print('getting GHRP contribution data')
    cumulativeByWeek(dfGHRP, allFunders)
    endTotals()

# visualizations
def visualizations():
    print('creating visualizations')
    runViz()

def runAll():
    #flowUpdate()
    #covidCases()
    #GHRPFinancing()
    #visualizations()
    #covidStats()
    #plotDelays()
    endTotals()
    plotUSSpeed()

runAll()
print('done!')
