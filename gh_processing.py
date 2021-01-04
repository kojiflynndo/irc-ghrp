'''
File for processing the JSONs from @markbrough's GHRP data
Outpus csv of funding timeline by flow ID

Last change: 30 December 2020
'''
import requests
import json
import pandas as pd
import pickle
import os
import time
import datetime as dt


def process():
    start = time.time()

    #read in list of SHAs as list named commits
    f_loc = os.getcwd() + '/output/gh_sha.txt'
    with open(f_loc, 'rb') as fp:
        commits = pickle.load(fp)

    FILES_URL = "https://github.com/markbrough/covid19-data/blob/{}/fts-emergency-911.json?raw=true"

    df = pd.DataFrame(columns=['id', 'source', 'destination', 'status',
                                'pledge_date','commit_date','paid_date',
                                'pledge_amount','commit_amount', 'paid_amount'
                                ])

    count = 1
    change = 0
    for i in range(len(commits)-1):
        sha = commits[i]
        #print('SHA', count, '/', len(commits))
        count +=1

        commit_file = requests.get(FILES_URL.format(sha)).json() #iterates through all the SHAs in commits and scrapes each one as a JSON file
        flows = commit_file['data']['flows'] #extracts just the flows data

        count2 = 1
        for flow in flows:
            #print('Flow', count2, '/', len(flows))
            count2 += 1

            id = flow['id']
            amount = flow['amountUSD']
            status = flow['status']
            source = flow['sourceObjects'][0]['name']
            destination = flow['destinationObjects'][0]['name']
            date = dt.datetime.strptime(flow['date'][:-10], '%Y-%m-%d').date()

            if ((df['id']==id) & (df['status']==status)).any():
                pass

            elif (id in df.values) and ((df['id']==id) & (df['status']!=status)).any():
                change += 1
                #print('Updating ID:', id, 'to', status)
                df.loc[(df.id==id), 'status'] = status
                if status=='pledge':
                    df.loc[(df.id==id), 'pledge_date'] = date
                    df.loc[(df.id==id), 'pledge_amount'] = amount
                elif status=='commitment':
                    df.loc[(df.id==id), 'commit_date'] = date
                    df.loc[(df.id==id), 'commit_amount'] = amount
                elif status=='paid':
                    df.loc[(df.id==id), 'paid_date'] = date
                    df.loc[(df.id==id), 'paid_amount'] = amount

            elif (id not in df.values):
                if status=='pledge':
                    temp = pd.DataFrame([[id, source, destination, status,
                                            date, None, None,
                                            amount, None, None
                                        ]],
                                columns=['id', 'source', 'destination', 'status',
                                        'pledge_date','commit_date','paid_date',
                                        'pledge_amount','commit_amount', 'paid_amount'
                                        ])
                elif status=='commitment':
                    '''
                    '''
                    temp = pd.DataFrame([[id, source, destination, status,
                                            None, date, None,
                                            None, amount, None
                                        ]],
                                columns=['id', 'source', 'destination', 'status',
                                        'pledge_date','commit_date','paid_date',
                                        'pledge_amount','commit_amount', 'paid_amount'
                                        ])
                elif status=='paid':
                    '''
                    '''
                    temp = pd.DataFrame([[id, source, destination, status,
                                            None, None, date,
                                            None, None, amount
                                        ]],
                                columns=['id', 'source', 'destination', 'status',
                                        'pledge_date','commit_date','paid_date',
                                        'pledge_amount','commit_amount', 'paid_amount'
                                        ])

                df = df.append(temp)

    loc = os.getcwd() + '/output/contribution_dates.csv'
    df.reset_index(drop=True, inplace=True)
    df.to_csv(loc)
    print('Saved to', loc)

    end = time.time()
    print(end-start)
