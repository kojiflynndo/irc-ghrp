import pandas as pd
import datetime as dt
import plotly.express as px
import os
import numpy as np
import openpyxl


def sumFunding():
    print('Funding')
    fundersDF = pd.read_csv(os.getcwd() + '/output/cumulative_funding_weekly.csv')

    dates = {}

    for i in fundersDF.index:

        d = fundersDF['date'][i]

        total = fundersDF['all_total'][i]
        committed = fundersDF['all_committed'][i]
        paid = fundersDF['all_paid'][i]


        if np.isnan(committed):
            print('nan!! c')

        if np.isnan(paid):
            print('nan!! p')

        if d not in dates:
            dates[d] = [0, 0, 0]

        dates[d][0] += total
        dates[d][1] += committed
        dates[d][2] += paid

    funding_series = pd.DataFrame(columns = ['date', 'all_total', 'all_committed', 'all_paid'])

    for k, v in dates.items():
        temp = pd.DataFrame([[k, v[0], v[1], v[2]]],

                columns = ['date', 'all_total', 'all_committed', 'all_paid'])

        funding_series = funding_series.append(temp)

    funding_series.to_csv(os.getcwd() + '/output/for_di/funding_series.csv', index=False)


def sumCovidContinent():
    countriesDF = pd.read_csv(os.getcwd() + '/output/covid-cases.csv')

    continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America']

    for continent in continents:
        print(continent)

        dates = {}

        for i in countriesDF.index:

            entry = countriesDF['continent'][i]

            if entry != continent:
                continue

            d = countriesDF['date'][i]
            cases = countriesDF['total_cases'][i]
            deaths = countriesDF['total_deaths'][i]

            if np.isnan(cases):
                cases = 0
            if np.isnan(deaths):
                deaths = 0

            if d not in dates:
                dates[d] = [0, 0]

            dates[d][0] += cases
            dates[d][1] += deaths

        covid_series = pd.DataFrame(columns = ['date', 'total_cases_ghrp', 'total_deaths_ghrp'])

        for k, v in dates.items():
            temp = pd.DataFrame([[k, v[0], v[1]]],

                    columns = ['date', 'total_cases_ghrp', 'total_deaths_ghrp'])

            covid_series = covid_series.append(temp)

        covid_series.to_csv(os.getcwd() + '/output/for_di/covid_cases_series_' + continent + '.csv', index=False)

def sumCovidTotal():
    print('All GHRP Countries')
    countriesDF = pd.read_csv(os.getcwd() + '/output/covid-cases.csv')

    countriesDF.fillna(0)

    dates = {}

    for i in countriesDF.index:

        d = countriesDF['date'][i]

        cases = countriesDF['total_cases'][i]
        deaths = countriesDF['total_deaths'][i]

        if np.isnan(cases):
            #print('gotcha c',i)
            cases = 0

        if np.isnan(deaths):
            #print('gotcha d',i)
            deaths = 0

        if d not in dates:
            print('adding', d)
            dates[d] = [cases, deaths]
            print(dates[d])
        else:
            dates[d][0] += cases
            dates[d][1] += deaths

        if np.isnan(cases):
            print('case slipped through', i)
        elif np.isnan(deaths):
            print('\ndeath slipped through', i)
            print(countriesDF['location'][i], countriesDF['date'][i])
            print(type(deaths))

    covid_series = pd.DataFrame(columns = ['date', 'total_cases_ghrp', 'total_deaths_ghrp'])

    for k, v in dates.items():
        temp = pd.DataFrame([[k, v[0], v[1]]],

                columns = ['date', 'total_cases_ghrp', 'total_deaths_ghrp'])


        covid_series = covid_series.append(temp)

    covid_series.to_csv(os.getcwd() + '/output/for_di/covid_cases_series.csv', index=False)

sumCovidTotal()
sumCovidContinent()
sumFunding()
