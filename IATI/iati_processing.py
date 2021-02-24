'''
File for processing IATI data, creating dates for each flow

Last change: 10 February 2021
'''
import os
import pandas as pd
import datetime as dt

from ghrp_tracker import getMondays

def process_ngo(df, name):

    m = getMondays()

    dict = {}

    for monday in m:

        # key:

        # 0: date, 1: org,
        # 2: total_inflow, 3: total_outflow
        # 4. inc_commitment 5. received
        # 6. out_commitment 7. disbursed 8. expenditure
        # 9. net_flow_total 10. net_cash

        dict[monday] = [monday, '',
                        0, 0,
                        0, 0,
                        0, 0, 0,
                        0, 0]

        for i, row in df.iterrows():

            date = dt.datetime.strptime(str(df['transaction_date'][i]),
                '%Y-%m-%d').date()
            transcode = df['transaction_type_code'][i]
            val = df['value_USD'][i]

            dict[monday][1] = df['reporting_org_text'][i]

            if date <= monday:
                # transcode (transaction_type_code) key:
                #   inflow
                #       1: incoming funds, 11: incoming commitment 13: incoming pledge
                #   outflow
                #       2. outgoing commitment 3. disbursement 4. expenditure

                if transcode == 1 or transcode == 11 or transcode == 13:
                    dict[monday][2] += val

                    if transcode == 1:
                        dict[monday][5] += val

                    elif transcode == 11:
                        dict[monday][4] += val


                elif transcode == 2:
                    dict[monday][3] += val
                    dict[monday][6] += val

                elif transcode == 3:
                    dict[monday][3] += val
                    dict[monday][7] += val

                elif transcode == 4:
                    dict[monday][3] += val
                    dict[monday][8] += val

        dict[monday][9] = dict[monday][2] - dict[monday][3]
        dict[monday][10] = dict[monday][5] - dict[monday][7] - dict[monday][8]


    output = pd.DataFrame.from_dict(dict, orient = 'index',

                columns = ['date', 'org',
                'total_inflow', 'total_outflow',
                'inc_commitment', 'received',
                'out_commitment', 'disbursed', 'expenditure',
                'net_flow_total', 'net_cash']

                                        )
    output.to_csv(os.getcwd() + '/output/iati_speed/' + name + '_speed.csv', index = False)




def process_funder(df, name):
    # We want the dataframe columns to be something like:
    # [id, commit, 25pc, 50pc, 75pc, 100pc, total]

    com_count = 0

    # dictionary to track each flow
    # key:

    # 0: source, 1: destination,
    # 2: commit date, 3: total value, 4: paid so far
    # 5. 10pc, 6. 20pc, 7. 30pc, 8. 40pc 9. 50pc
    # 10. 60pc, 11. 70pc, 12. 80pc, 13. 90pc, 14. 100pc
    # 15. commit_updates
    # 16. recipient_type

    ids = {}

    for i, row in df.iterrows():


        identity = df['iati_identifier'][i]
        date = df['transaction_date'][i]
        transcode = df['transaction_type_code'][i]
        val = df['value_USD'][i]
        source = df['reporting_org_text'][i]
        destination = df['receiver_text'][i]
        destination_type = df['receiver_type'][i]

        if identity not in ids:
            # key:

            # 0: source, 1: destination,
            # 2: commit date, 3: total value, 4: paid so far
            # 5. 10pc, 6. 20pc, 7. 30pc, 8. 40pc 9. 50pc
            # 10. 60pc, 11. 70pc, 12. 80pc, 13. 90pc, 14. 100pc
            # 15. commit_updates
            # 16. recipient_type

            ids[identity] = [source, destination,
                                '', 0, 0,
                                '', '', '', '', '',
                                '', '', '', '', '',
                                0,
                                '']

        # if this is the first instance and this is a commitment, set the
        # date committed and total value accordingly
        if (transcode == 2) and (ids[identity][3] == 0):
            ids[identity][2] = date
            ids[identity][3] = val

        # if this is not the first instance and this is a commitment, update
        # the total value, but do not change the date of the intial commitment
        elif (transcode == 2):
            ids[identity][3] += val
            ids[identity][15] += 1

        # if this is a disbursement, add it to the total amount paid so far
        elif (transcode == 3):
            ids[identity][4] += val


        # check if the total amount paid so far reaches 100, 90, 80... 10 percent
        # if so, add the date to the appropriate column
        if ids[identity][3] == 0:
            continue

        for i, pc in enumerate([1.0, 0.9, 0.8, 0.7, 0.6,
                                0.5, 0.4, 0.3, 0.2, 0.1]):
            if (ids[identity][4]/ids[identity][3] >= pc):

                ids[identity][14-i] = date


    outputdf = pd.DataFrame(
        columns = ['id',
                'source', 'destination',
                'commit_date', 'total_value', 'paid_to_date',
                'pc10', 'pc20', 'pc30', 'pc40', 'pc50',
                'pc60', 'pc70', 'pc80', 'pc90', 'pc100',
                'commit_updates']
    )


    for k, v in ids.items():

        dates = {}

        for i, pc in enumerate([1.0, 0.9, 0.8, 0.7, 0.6,
                                0.5, 0.4, 0.3, 0.2, 0.1]):

            key = 'pc' + str(pc)

            dates[key] = v[14 - i]


        prev = v[14]

        for day, value in dates.items():
            if value == '':
                dates[day] = prev
            else:
                prev = dates[day]

        temp = pd.DataFrame(
            columns = ['id',
                    'source', 'destination',
                    'commit_date', 'total_value', 'paid_to_date',
                    'pc10', 'pc20', 'pc30', 'pc40', 'pc50',
                    'pc60', 'pc70', 'pc80', 'pc90', 'pc100',
                    'commit_updates',
                    'receiver_type'],

            data = [[k,
                    v[0], v[1],
                    v[2], v[3], v[4],
                    dates['pc0.1'], dates['pc0.2'], dates['pc0.3'], dates['pc0.4'], dates['pc0.5'],
                    dates['pc0.6'], dates['pc0.7'], dates['pc0.8'], dates['pc0.9'], dates['pc1.0'],
                    v[15],
                    v[16]
                            ]])

        outputdf = outputdf.append(temp)

    outputdf.to_csv(os.getcwd() + '/output/iati_speed/' + name + '_speed.csv', index = False)




def main():
    funders = ['echo', 'germany', 'usaid']

    ngos = ['actionaid', 'drc', 'novib', 'unhcr']

    print('executing funders')
    for name in funders:
        print(name)
        df = pd.read_csv(os.getcwd() + '/input/' + name + '_iati.csv')
        process_funder(df, name)

    print('executing ngos')
    for name in ngos:
        print(name)
        df = pd.read_csv(os.getcwd() + '/input/' + name + '_iati.csv')
        process_ngo(df, name)

main()
