'''
'''
from ghrp_tracker import *
from irc_style import *
from fts_analysis import updatedFlows

import pandas as pd
import datetime as dt
import os
import altair as alt
import openpyxl
import toolz

today = str(dt.datetime.now().date())
start = dt.date(2020, 3, 25)
last_day = dt.date(2020, 12, 31)

# allows larger datasets
from altair import pipe, limit_rows, to_values
t = lambda data: toolz.curried.pipe(data, limit_rows(max_rows=1000000), to_values)
alt.data_transformers.register('custom', t)
alt.data_transformers.enable('custom')

def endTotals():
    '''
    For checking end totals against DI data
    '''
    temp = pd.read_csv(os.getcwd() + '/output/cumulative_funding_weekly.csv')
    temp.reset_index(drop=True, inplace=True)
    temp["date"] = pd.to_datetime(temp["date"])
    endTotals = temp.copy()
    for i in endTotals.index:
        if endTotals['date'][i] != last_day:
            endTotals.drop([i], inplace=True)
    loc = os.getcwd() + '/output/end_totals.csv'
    endTotals.to_csv(loc, index=False)
    print('saved to', loc)


def printDelays(commit_to_now):
    '''
    Takes dictionary commit_to_now from plotDelays, prints out summary
        statistics of delays in disbursements.
    '''

    commit_to_now_count = 0
    commit_to_now_total = dt.timedelta(0)
    for k, v in commit_to_now.items():
        commit_to_now_count+=1
        commit_to_now_total+=v

    commit_to_now_total=commit_to_now_total.days

    for_median = [val.days for val in commit_to_now.values()]

    print(('Mean time since committed: {}').format(commit_to_now_total/commit_to_now_count))
    print(('Median time since committed: {}').format(np.median(for_median)))
    print('Max commit to now:', max(commit_to_now.values()))
    print('Min commit to now:', min(commit_to_now.values()))


def plotDelays():
    '''
    '''
    df = pd.read_csv(os.getcwd() + '/output/contribution_dates.csv')
    now = dt.datetime.now().date()

    num = 0
    commit_to_now = {}

    for i in df.index:
        id = df['id'][i]

        pl = pd.notna(df['pledge_amount'][i])
        cm = pd.notna(df['commit_amount'][i])
        pa = pd.notna(df['paid_amount'][i])
        if pl:
            pld = dt.datetime.strptime(str(df['pledge_date'][i]), '%Y-%m-%d').date()
        if cm:
            cmd = dt.datetime.strptime(str(df['commit_date'][i]), '%Y-%m-%d').date()
        if pa:
            pad = dt.datetime.strptime(str(df['paid_date'][i]), '%Y-%m-%d').date()

        if (cm) and not (pa):
            if cmd < dt.date(2020, 3, 25):
                continue
            commit_to_now[id]=(now-cmd)

    printDelays(commit_to_now)

    data = pd.DataFrame(commit_to_now.items(), columns=['id','time'])
    data['time'] = data['time'].dt.days
    data=data[['id','time']]

    hist = alt.Chart(data).mark_bar(color='red').encode(
            x=alt.X('time:Q',  bin=alt.Bin(step=20), title='Days Since Committed and Not Paid'),
            y=alt.Y('count()', title='Number of Flows'),
            tooltip=['time:Q', 'count()']).properties(
            title='More than half of unpaid commitments have been outstanding for more than 170 days'
            )
    #hist.show()
    loc=os.getcwd()+ '/viz/commitDelay_'+today+'.html'
    hist.save(loc)
    print('saved to', loc)


def plotUnpaid():
    df = updatedFlows() #from fts_analysis
    df.reset_index(drop=True, inplace=True)

    df['percent_updated'] = df['updated_flows']/df['total_flows']
    df = df.sort_values(by=['percent_updated'])

    for i in df.index:
        if df['nonpaid_total_flows'][i] < 15:
            df.drop([i], inplace=True)
    df.reset_index(drop=True, inplace=True)

    unpaidpc = alt.Chart(df).mark_bar(color='red').encode(
            x=alt.X('source',
                    axis=alt.Axis(labelAngle=45),
                    sort='-y'),
            y=alt.Y('pc_flows_nonpaid', axis=alt.Axis(title='Percentage of Flows Unpaid',format='%')),
            tooltip=['pc_flows_nonpaid','paid_flows','total_flows']
            ).properties(
            title='Funders have not disbursed the majority of their financial flows'
            )
    unpaidNum = alt.Chart(df).mark_bar(color='red').encode(
            x=alt.X('source',
                    axis=alt.Axis(labelAngle=45),
                    sort='-y'),
            y=alt.Y('nonpaid_flows'),
            tooltip=['nonpaid_flows','paid_flows','total_flows']
            ).properties(
            title='Number of Flows Unpaid by Funder*'
            )

    unpaidpc.save(os.getcwd() + '/viz/unpaidPc_'+today+'.html')
    unpaidNum.save(os.getcwd() + '/viz/unpaidNum_'+today+'.html')


def plotUSSpeed():
    '''
    '''
    df = pd.read_csv(os.getcwd() + '/output/contribution_dates.csv')

    commit_to_paid = {}
    pledge_to_commit = {}
    pledge_to_paid = {}

    backwards = []

    for i in df.index:
        if df['source'][i]=='United States of America, Government of':
            id = df['id'][i]
            # check if value exists
            pl = pd.notna(df['pledge_date'][i])
            cm = pd.notna(df['commit_date'][i])
            pa = pd.notna(df['paid_date'][i])
            if pl:
                pld = dt.datetime.strptime(str(df['pledge_date'][i]), '%Y-%m-%d').date()
            if cm:
                cmd = dt.datetime.strptime(str(df['commit_date'][i]), '%Y-%m-%d').date()
            if pa:
                pad = dt.datetime.strptime(str(df['paid_date'][i]), '%Y-%m-%d').date()

            if (pa) and ((not cm) and (not pl)):
                #print(id,'was paid immediately')
                continue
            elif pa and cm:
                if cmd>pad:
                    backwards.append(id)
                    print(id, 'backwards update?')
                    continue
                commit_to_paid[id] = pad-cmd
            elif cm and pl:
                if pld>cmd:
                    backwards.append(id)
                    print(id, 'backwards update?')
                    continue
                pledge_to_commit[id] = cmd-pld
            elif pa and pl:
                if pld>pad:
                    backwards.append(id)
                    print(id, 'backwards update?')
                    continue
                pledge_to_paid[id] = pad - pld

    commit_to_paid_total = dt.timedelta(0)
    commit_to_paid_count = 0
    pledge_to_commit_total = dt.timedelta(0)
    pledge_to_commit_count = 0
    pledge_to_paid_total = dt.timedelta(0)
    pledge_to_paid_count = 0

    for k, v in commit_to_paid.items():
        commit_to_paid_count+=1
        commit_to_paid_total+=v

    ls = [int(i.days) for i in commit_to_paid.values()]

    print('Mean commit to paid:', commit_to_paid_total/commit_to_paid_count)
    print('Standard deviation:', int(np.std(ls)), 'days')
    print('Max commit to paid:', max(commit_to_paid.values()))
    print('Min commit to paid:', min(commit_to_paid.values()))

    data = pd.DataFrame(commit_to_paid.items(), columns=['id','td'])
    data['time'] = data['td'].dt.days

    data=data[['id','time']]
    #bar = alt.Chart(data).mark_bar().encode(x=alt.X('id:N', sort='-y'), y='time')
    bar = alt.Chart(data).mark_bar().encode(
            x=alt.X('time:Q', bin=True, title='Days Until Payment'),
            y=alt.Y('count()', title='Number of Flows'),
            tooltip=['time:Q', 'count()']).properties(
            title='Days from Commitment to Payment, United States'
            )
    bar.save(os.getcwd() + '/viz/usSpeed_'+today+'.html')


def getNGOdata(df, funders):
    '''
    We want data with columns: [date, class, amount]
    Where date is the date, class is the type of organization (UN org, WHO,
        Red Cross, NGOs), and amount is the amount of funding.
    Each date should have n entries, where n is the number of classes of
        organization--as of now, n=4
    To do this, we want to do something similar to cumulativeByWeek.
    '''
    dfDaily = fundingByDay(df, funders)
    dfDaily.reset_index(inplace=True)

    forNorm = pd.DataFrame(columns = ['date', 'class', 'amount'])
    m = getMondays()

    for monday in m:
        dict = {'united_nations':0,'world_health_organization':0,'red_cross':0,
                'ngo':0,'government':0}
        for i in dfDaily.index:
            val = dfDaily['total_amount'][i]
            date = dt.datetime.strptime(str(dfDaily['date'][i]),'%Y-%m-%d').date()
            impl = dfDaily['implementer'][i]
            if date<=monday:
                if dfDaily['ngo'][i] == True:
                    dict['ngo']+=val
                elif (('United Nations' in impl) or
                    ('Office for the Coordination of Humanitarian Affairs' in impl)
                    or ('World Food Programme' in impl) or
                    ('International Organization for Migration' in impl)):
                    dict['united_nations']+=val
                elif 'World Health Organization' in impl:
                    dict['world_health_organization']+=val
                elif 'Red Cross' in impl:
                    dict['red_cross']+=val
                elif (('Government of' in impl) or ('Swiss Development' in impl)
                    or ('Palestinian territory' in impl)):
                    dict['government']+=val
                else:
                    dict['other']+=val
                    print('unknown category', impl)

        for k, v in dict.items():
            temp = pd.DataFrame([[monday, k, v]],
                        columns = ['date', 'class', 'amount'])
            forNorm = forNorm.append(temp)

    loc = os.getcwd() + '/output/ngo_normalized_' + today +'.csv'
    forNorm.to_csv(loc, index=False)
    print('saved to', loc)
    return forNorm


def plotNGO(df, allFunders):
    '''
    '''
    dfNGO = getNGOdata(df, allFunders)
    dfNGO.reset_index(drop=True, inplace=True)

    for i in dfNGO.index:
        d = dfNGO['date'][i]
        if d<=start:
            dfNGO.drop([i], inplace=True)
    dfNGO["date"] = pd.to_datetime(dfNGO["date"])

    ngoNorm = alt.Chart(dfNGO).mark_area().encode(
                x='date:T',
                y=alt.Y('amount:Q',
                        axis=alt.Axis(title='Percentage of Funding Received', format='%'),
                        stack='normalize'),
                color=alt.Color('class:N',
                    legend=alt.Legend(title='Recipient Organization Classes')),
                tooltip=['class:N', 'date:T',
                        alt.Tooltip('amount:Q', format='$,')]).properties(
                title='NGOs have received a small fraction of direct funding while UN agencies have received the most funding'
                )

    ngoArea = alt.Chart(dfNGO).mark_area().encode(
                x='date:T',
                y=alt.Y('amount:Q',
                        axis=alt.Axis(title=None, format='$s'),
                        scale=alt.Scale(domain=(0, 11000000000))),
                color=alt.Color('class:N',
                    legend=alt.Legend(title='Recipient Organization Classes')),
                tooltip=['class:N', 'date:T',
                        alt.Tooltip('amount:Q', format='$,')]).properties(
                title='Funding by Recipient Organization Classes'
                )

    #ngoArea.show()
    ngoArea.save(os.getcwd() + '/viz/ngoArea_' + today + '.html')
    #ngoNorm.show()
    ngoNorm.save(os.getcwd()+ '/viz/ngoNormalized' + today + '.html')


def plotCovid():
    '''
    '''
    dfCov = pd.read_csv(os.getcwd() + '/output/covid-cases.csv')
    dfCov["date"] = pd.to_datetime(dfCov["date"])

    #cases by country
    countries = alt.Chart(dfCov).mark_area().encode(
            x=alt.X('date', axis=alt.Axis(title=None)),
            y=alt.Y('total_cases', axis=alt.Axis(title='COVID-19 Cases', format='s')),
            color=alt.Color('location',
            legend=None),
            tooltip=['location','continent','date:T',
            alt.Tooltip('total_cases', format=','),
            alt.Tooltip('total_deaths', format=',')]).properties(
                title='Aid disbursements have failed to keep pace with the increasing scale of the COVID-19 crisis.'
            )
    #countries.show()
    countries.save(os.getcwd() + '/viz/casesArea_' + today + '.html')

    #cases with continent facets
    con_facet = alt.Chart(dfCov).mark_area().encode(
            x=alt.X('date', axis=alt.Axis(title=None)),
            y=alt.Y('total_cases', axis=alt.Axis(title=None)),
            color=alt.Color('location', legend=None),
            column=alt.Column('continent', title=None),
            tooltip=['location','continent','date:T',
            alt.Tooltip('total_cases', format=','),
            alt.Tooltip('total_deaths', format=',')]).properties(
                title='Reported COVID-19 cases continue to rise in GHRP countries, especially in South America',
                width=150, height=250
            )
    #con_facet.show()
    con_facet.save(os.getcwd() + '/viz/casesFacets_' + today + '.html')

    return countries


def plotCumulative(df, funders):
    '''
    '''
    temp = pd.read_csv(os.getcwd() + '/output/cumulative_funding_weekly.csv')
    dfCumlt = temp.copy()
    dfCumlt.reset_index(drop=True, inplace=True)
    dfCumlt["date"] = pd.to_datetime(dfCumlt["date"])

    #dfCumlt.to_csv(os.getcwd() + '/output/for_cumulative_plot.csv', index=False)

    #makes a few aesthetic adjustments to dfCumlt
    dfCumlt.rename(columns= {'all_paid': 'paid',
                            'all_committed': 'committed',
                            'all_total': 'total',
                            'actor': 'funder'},
                            inplace = True)
    for i in dfCumlt.index:
        if 'Government of' in dfCumlt['funder'][i]:
            dfCumlt.at[i, 'funder'] = dfCumlt['funder'][i].replace(', Government of', '')

    #creates base chart of paid contributions
    c_paid = alt.Chart(dfCumlt).mark_area().encode(
        x=alt.X('date'),
        y=alt.Y('paid',
            axis=alt.Axis(format='$,s', title='Paid Contributions'),
            scale=alt.Scale(domain=(0, 11000000000))),
        color=alt.Color('funder', legend=None),
        tooltip=['funder', 'date:T',
                alt.Tooltip('paid:Q', format='$,'),
                alt.Tooltip('committed:Q', format='$,'),
                alt.Tooltip('total:Q', format='$,')]
        )#.properties(title='GHRP Paid Contributions by Funder')

    #creates df and chart for combined totals
    mondays = getMondays()

    d = {}
    for monday in mondays:
        # [0]: paid, [1]: committed, [2]: total
        d[monday] = [0,0,0]
        for i in dfCumlt.index:
            date = dfCumlt['date'][i]
            if date == monday:
                d[monday][0] += dfCumlt['paid'][i]
                d[monday][1] += dfCumlt['committed'][i]
                d[monday][2] += dfCumlt['total'][i]
    dfCombined = pd.DataFrame(columns = ['date','paid','committed','total'])
    for k, v in d.items():
        temp = pd.DataFrame([[k, v[0], v[1], v[2]]],
                columns = ['date','paid','committed','total'])
        dfCombined = dfCombined.append(temp)
    text = pd.DataFrame([[None, None, None, None, 'Total Paid and Committed']],
                columns = ['date','paid','committed','total', 'text'])
    dfCombined = dfCombined.append(text)
    dfCombined["date"] = pd.to_datetime(dfCombined["date"])
    #dfCombined.to_csv('combined_viz.csv', index=False)

    combined = alt.Chart(dfCombined).mark_line(
                color='blue',
                strokeWidth=4,
                opacity = .4,).encode(
                x=alt.X('date'),
                y=alt.Y('total'),
                tooltip=['date:T',
                        alt.Tooltip('total:Q', format='$,'),
                        alt.Tooltip('paid:Q', format='$,'),
                        alt.Tooltip('committed:Q', format='$,')]
                )
    #label for combined line
    c_text = alt.Chart(pd.DataFrame(
            {'text': ['Total Paid and Committed Funding']})
            ).mark_text(
            fontSize = 12,
            fontWeight = 400,
            color = 'black',
            fillOpacity = 1,
            dx = 50,
            ).encode(text='text')


    #adds line for GHRP target
    line = alt.Chart(pd.DataFrame(
                {'y': [9500000000], 'text': ['GHRP Requirement ($9.5 billion)']})
                ).mark_rule(
                    color='red',
                    opacity = .5,
                    strokeWidth = 3
                    ).encode(y='y')
    #label for line
    l_text = line.mark_text(
            dx = 275,
            dy = -30,
            baseline = 'line-top',
            fontSize = 14,
            fontWeight = 600, #bold
            color = 'black',
            fillOpacity = .8
            ).encode(text='text')

    fig = c_paid + combined + line
    #fig.show()
    fig.save(os.getcwd() + '/viz/cumulativeFunding_' + today + '.html')

    return fig


def stacked(df, allFunders):
    '''
    '''
    cases = plotCovid()
    funding = plotCumulative(df, allFunders)

    chart = alt.vconcat(cases, funding).resolve_scale(
            color='independent').configure_view(
            stroke=None)
    #chart.show()
    chart.save(os.getcwd() + '/viz/stacked_' + today + '.html')


def runViz():
    alt.themes.enable('custom_irc')

    dfViz = pd.read_excel(os.getcwd() + '/input/contributions.xlsx', engine='openpyxl')
    dfViz = cleandf(dfViz)
    allFunders = getFunders(dfViz)

    #stacked(dfViz, allFunders)
    #plotNGO(dfViz, allFunders)
    #plotDelays()
    #plotUSSpeed()
    #plotUnpaid()
    plotCovid()

runViz()
