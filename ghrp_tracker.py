'''

Last edit: 30 December 2020
'''

import pandas as pd
import datetime as dt
import plotly.express as px
import os
import numpy as np
import openpyxl

def isNGO(implementer):
    '''
    Helper
    Takes the name of an implementer. If the implementer is in the list of
        non-NGOs, returns False. Otherwise, returns True.
    '''
    notNGO = [
        'United Nations', 'Office for the Coordination of Humanitarian Affairs',
        'World Food Programme', 'International Organization for Migration',
        'World Health Organization', 'Red Cross',
        'Swiss Development Cooperation', 'Government of',
        'Palestinian territory'
        ]

    for n in notNGO:
        if n in implementer:
            return False
    return True


def getMondays():
    '''
    Helper
    Creates a list with a date object for each Monday in 2020, plus 31 December
    Returns that list.
    '''

    year = 2020
    today = dt.datetime.now().date()

    first_mon = dt.date(2020, 1, 6)
    dtObj = first_mon

    mondays = []

    while dtObj < today:
        mondays.append(dtObj)
        dtObj += dt.timedelta(days=7)
    mondays.append(dt.date(2020, 12, 31))
    mondays.append(dt.date(2020, 12, 30))
    return mondays


def getFunders(df):
    '''
    Given the DI dataset df, returns list of all funders
    '''

    allFunders = []
    unknowns = 0
    for i in df.index:
        f = df['funder'][i]
        if f is np.nan:
            unknowns += 1
            df.at[i, 'funder'] = 'unknown'
            if 'unknown' not in allFunders:
                allFunders.append('unknown')
            continue
        elif f not in allFunders:
            allFunders.append(f)

    return allFunders


def covidStats():
    '''
    Prints stats on COVID in GHRP countries and South America relative to
        world
    '''
    ghrpCountries = ['Afghanistan', 'Angola', 'Argentina', 'Aruba', 'Bangladesh',
                    'Benin', 'Bolivia', 'Brazil', 'Burundi', 'BurkinaFaso',
                    'Cameroon', 'Central African Republic', 'Chad', 'Chile',
                    'Colombia', 'Costa Rica', 'Curacao', 'Djibouti',
                    'Dominican Republic', 'DPR Korea', 'Democratic Republic of Congo',
                    'Ecuador', 'Egypt', 'Ethiopia', 'Guyana', 'Haiti', 'Iran',
                    'Iraq', 'Jordan', 'Kenya', 'Lebanon', 'Liberia', 'Libya',
                    'Mali', 'Mexico', 'Mozambique', 'Myanmar', 'Niger', 'Nigeria',
                    'Palestine', 'Pakistan', 'Panama', 'Paraguay', 'Peru',
                    'Philippines', 'Congo', 'Rwanda', 'SierraLeone', 'Somalia',
                    'SouthSudan', 'Sudan', 'Syria', 'Tanzania',
                    'Trinidad and Tobago', 'Turkey', 'Uganda', 'Ukraine', 'Uruguay',
                    'Venezuela', 'Yemen', 'Zambia', 'Zimbabwe']

    covidDF = pd.read_csv(os.getcwd() + '/output/covid-cases.csv')
    owiddf = pd.read_csv(os.getcwd() + '/input/owid-covid-data.csv')

    world = owiddf.copy().loc[owiddf['iso_code']=='OWID_WRL']
    world_cases = int(world.copy().loc[world['date']=='2020-12-30', 'total_cases'])
    world_deaths = int(world.copy().loc[world['date']=='2020-12-30', 'total_deaths'])

    ghrp_cases = 0
    ghrp_deaths = 0
    southam_cases = 0
    southam_deaths = 0
    begin_deaths = 0

    for i in covidDF.index:
        if covidDF['location'][i] in ghrpCountries:
            if covidDF['date'][i]=='2020-12-30':
                ghrp_cases += covidDF['total_cases'][i]
                ghrp_deaths += covidDF['total_deaths'][i]
                if covidDF['continent'][i]=='South America':
                    southam_cases+= covidDF['total_cases'][i]
                    southam_deaths+=covidDF['total_deaths'][i]
            elif covidDF['date'][i]=='2020-03-30':
                if pd.isna(covidDF['total_deaths'][i]):
                    continue
                begin_deaths += covidDF['total_deaths'][i]

    print(('Cases: {} / {} : {}').format(ghrp_cases,world_cases, ghrp_cases/world_cases))
    print(('Deaths: {} / {} : {}').format(ghrp_deaths,world_deaths,ghrp_deaths/world_deaths))
    print(('Deaths have multipled by {} since March 23--{} to {}').format(ghrp_deaths/begin_deaths, begin_deaths, ghrp_deaths))
    print(('South America: {} percent of cases and {} percent of deaths worldwide').format(southam_cases/world_cases, southam_deaths/world_deaths))


def cumulativeCovidCases():
    '''
    Reads in Our World in Data dataset. For each GHRP country, gets
        total cases for each Monday of the year so far.
    Outputs:    1. df with total weekly cases
                2. csv with total weekly cases
    '''
    #ghrp countries--there's no data on North Korea in the OWID csv
    ghrpCountries = ['Afghanistan', 'Angola', 'Argentina', 'Aruba', 'Bangladesh',
                    'Benin', 'Bolivia', 'Brazil', 'Burundi', 'BurkinaFaso',
                    'Cameroon', 'Central African Republic', 'Chad', 'Chile',
                    'Colombia', 'Costa Rica', 'Curacao', 'Djibouti',
                    'Dominican Republic', 'DPR Korea', 'Democratic Republic of Congo',
                    'Ecuador', 'Egypt', 'Ethiopia', 'Guyana', 'Haiti', 'Iran',
                    'Iraq', 'Jordan', 'Kenya', 'Lebanon', 'Liberia', 'Libya',
                    'Mali', 'Mexico', 'Mozambique', 'Myanmar', 'Niger', 'Nigeria',
                    'Palestine', 'Pakistan', 'Panama', 'Paraguay', 'Peru',
                    'Philippines', 'Congo', 'Rwanda', 'SierraLeone', 'Somalia',
                    'SouthSudan', 'Sudan', 'Syria', 'Tanzania',
                    'Trinidad and Tobago', 'Turkey', 'Uganda', 'Ukraine', 'Uruguay',
                    'Venezuela', 'Yemen', 'Zambia', 'Zimbabwe']

    owiddf = pd.read_csv(os.getcwd() + '/input/owid-covid-data.csv')
    mondays = getMondays()

    for i in owiddf.index:
        d = owiddf['date'][i]
        date = dt.datetime.strptime(d, '%Y-%m-%d').date()
        l = owiddf['location'][i]
        if l not in ghrpCountries or date not in mondays:
            owiddf.drop([i], inplace=True)

    owiddf.reset_index(drop=True, inplace=True)
    owiddf.to_csv(os.getcwd() + '/output/covid-cases.csv', index = False)
    print('saved to', os.getcwd() + '/output/covid-cases.csv')
    return owiddf


def cumulativeByWeek(df, funders):
    '''
    Uses the fundingByDay function to get total funding by day per actor, then
        adds up cumulative funding by each Monday of the year so far.
    Outputs:    1. df with cumulative weekly funding
                2. csv with cumulative weekly funding
    '''

    dfDaily = fundingByDay(df, funders)
    dfDaily.reset_index(inplace=True)

    cumulative = pd.DataFrame(columns = ['actor','date',
                    'all_total','all_committed','all_paid',
                    'all_pc_paid',
                    'ngo_total','ngo_committed','ngo_paid',
                    'ngo_pc_paid',
                    'ngo_pc_of_total','ngo_pc_of_paid'])

    m = getMondays() # list of mondays
    for f in funders: # for each funder
        d = {}  # create new dictionary
        for monday in m: # for each monday
            d[monday] = [0,0,0,0,0,0] # create new entry in dictionary
            for i in dfDaily.index:
                date = dt.datetime.strptime(str(dfDaily['date'][i]),'%Y-%m-%d').date()
                funder = dfDaily['actor'][i]
                if funder==f and date<=monday:
                    num = dfDaily['total_amount'][i]
                    implementer = dfDaily['implementer'][i]
                    status = dfDaily['status'][i]
                    d[monday][0] += num
                    if status=='commitment' or status=='pledge':
                        d[monday][1] += num
                        if dfDaily['ngo'][i]==True:
                            d[monday][4] += num
                            d[monday][3] += num
                    elif status=='paid':
                        d[monday][2] += num
                        if dfDaily['ngo'][i]==True:
                            d[monday][5] += num
                            d[monday][3] += num
                    else:
                        print('uncategorized funding!', f, num, status)
        for k, v in d.items():
            try:
                ngo_pc_paid = v[5]/v[3]
            except:
                ngo_pc_paid = 0
            try:
                all_pc_paid = v[2]/v[0]
            except:
                all_pc_paid = 0
            try:
                ngo_pc_of_total = v[3]/v[0]
            except:
                ngo_pc_of_total = 0
            try:
                ngo_pc_of_paid = v[5]/v[2]
            except:
                ngo_pc_of_paid = 0

            temp = pd.DataFrame([[f, k, # k should be a monday
                                v[0], v[1], v[2],
                                all_pc_paid,
                                v[3], v[4], v[5],
                                ngo_pc_paid,
                                ngo_pc_of_total, ngo_pc_of_paid]],
                    columns = ['actor','date',
                                'all_total','all_committed','all_paid',
                                'all_pc_paid',
                                'ngo_total','ngo_committed','ngo_paid',
                                'ngo_pc_paid',
                                'ngo_pc_of_total','ngo_pc_of_paid'])
            cumulative = cumulative.append(temp)

    cumulative.to_csv(os.getcwd() + '/output/cumulative_funding_weekly.csv', index = False)
    print('saved to', os.getcwd() + '/output/cumulative_funding_weekly.csv')
    return cumulative


def fundingByDay(df, funders):
    '''
    Takes DI dataset df and a list of funders. Iterates through original df
        and outputs new df with total funding by day for each funder.

    Outputs:    1. df with total funding by day for each funder
                2. csv with total funding by day for each funder
    '''

    daily = pd.DataFrame(columns = ['actor','date',
            'implementer','ngo','status','paid_amount','total_amount'])

    for f in funders:
        #Resets the dictionary
        dates = {}
        for i in df.index:
            #isolates for commitmens which have been paid
            if df['funder'][i] == f:
                day = df['date'][i]
                if day not in dates:
                    dates[day] = [None, None, None, 0, 0]

                dates[day][0] = df['implementer'][i]
                if isNGO(str(df['implementer'][i])):
                    dates[day][1] = True
                else:
                    dates[day][1] = False
                dates[day][2] = df['status'][i]
                if df['status'][i] == 'paid':
                    dates[day][3] += df['amount_usd'][i]
                dates[day][4] += df['amount_usd'][i]


        for k, v in dates.items():
            temp = pd.DataFrame([[f, k, v[0], v[1], v[2], v[3], v[4]]],
            columns = ['actor','date', 'implementer','ngo',
            'status','paid_amount', 'total_amount'])
            daily = daily.append(temp)

    daily.to_csv(os.getcwd() + '/output/funding_by_day.csv', index = False)

    return daily


def cleandf(df):
    '''
    Cleans the DI dataset df column names
    Returns the cleaned df
    '''
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace(',', '')

    return df


def main():
    '''
    Reads in the Development Initatives (DI) dataset and calls any relevant
        functions
    '''
    df = pd.read_excel(os.getcwd()+'/input/contributions.xlsx', engine='openpyxl')
    df = cleandf(df)

    allFunders = getFunders(df)

    print('running covid cases')
    cumulativeCovidCases()

    print('running ghrp funding')
    cumulativeByWeek(df, allFunders)
