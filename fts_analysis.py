'''
File for analyzing changes in FTS data
First runs scrape from gh_scraping, then process from gh_processing, then
    outputs a csv detailing funding speed by actor

Last change: 30 December 2020
'''

import pandas as pd
import os
import datetime as dt
import numpy as np
import altair as alt
from gh_processing import process
from gh_scraping import scrape

def updatedFlows():
    df = pd.read_csv(os.getcwd() + '/output/contribution_dates.csv')
    funders = {}

    for i in df.index:
        f = df['source'][i]
        # check if value exists
        pl = pd.notna(df['pledge_amount'][i])
        cm = pd.notna(df['commit_amount'][i])
        pa = pd.notna(df['paid_amount'][i])
        if pa:
            val = df['paid_amount'][i]
        elif cm:
            val = df['commit_amount'][i]
        elif pl:
            val = df['pledge_amount'][i]

        if f not in funders:
            funders[f] =    [0,0,0,
                            0,0,0,
                            0,0,0]

        funders[f][1]+=1
        funders[f][4]+=val

        if (pl and cm) or (pl and pa) or (cm and pa):
            funders[f][0]+=1
            funders[f][3]+=val

        # captures flows which are only committed
        if (cm) and ((not pa) and (not pl)):
            funders[f][7]+=1
        # captures flows which are only pledged
        elif (pl) and ((not pa) and (not cm)):
            funders[f][8]+=1
        elif pa:
            funders[f][6]+=1
        # ignores all flows which started out as paid
        if (pa) and ((not cm) and (not pl)):
            continue
        else:
            funders[f][2]+=1
            funders[f][5]+=val

    funding_speed = pd.DataFrame(columns=['source',
                                'updated_flows', 'total_flows', 'nonpaid_total_flows',
                                'updated_value', 'total_value', 'nonpaid_total_value',
                                'paid_flows', 'commit_only_flows', 'pledge_only_flows'])

    for f in funders.items():
        temp = pd.DataFrame(data=   [[f[0],
                                    f[1][0],f[1][1],f[1][2],
                                    f[1][3],f[1][4],f[1][5],
                                    f[1][6],f[1][7],f[1][8]]],
                            columns=['source',
                                    'updated_flows', 'total_flows', 'nonpaid_total_flows',
                                    'updated_value', 'total_value', 'nonpaid_total_value',
                                    'paid_flows', 'commit_only_flows', 'pledge_only_flows'])

        funding_speed = funding_speed.append(temp)

    funding_speed['pc_flows_paid'] = funding_speed['paid_flows']/funding_speed['total_flows']
    funding_speed['pc_flows_nonpaid'] = 1-funding_speed['pc_flows_paid']
    funding_speed['nonpaid_flows'] = funding_speed['commit_only_flows'] + funding_speed['pledge_only_flows']

    loc = os.getcwd() + '/output/funding_speed.csv'
    funding_speed.to_csv(loc, index=False)
    print('saved to', loc)

    return funding_speed
