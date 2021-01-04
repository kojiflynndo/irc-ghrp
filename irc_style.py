'''
Altair Custom Theme for IRC Charts
'''
import altair as alt

def irc_style():
    #typography
    font = 'Akzidenz-Grotesk Std Regular'
    titleFont = 'Akzidenz-Grotesk Std Regular' # 'Akzidenz-Grotesk Std Bold'
    labelFont = 'Akzidenz-Grotesk Std Regular'
    sourceFont = 'Akzidenz-Grotesk Std'


    #axes
    axisColor = '#000000'
    gridColor = '#DEDDDD'

    #colors
    tableau20 = ['#9edae5',
                '#17becf',
                '#dbdb8d',
                '#bcbd22',
                '#c7c7c7',
                '#7f7f7f',
                '#f7b6d2',
                '#e377c2',
                '#c49c94',
                '#8c564b',
                '#c5b0d5',
                '#9467bd',
                '#ff9896',
                '#d62728',
                '#98df8a',
                '#2ca02c',
                '#ffbb78',
                '#ff7f0e',
                '#aec7e8',
                '#1f77b4'
                ]
    plotly34 = ['#1f77b4',
                '#ff7f0e',
                '#2ca02c',
                '#d62728',
                '#9467bd',
                '#8c564b',
                '#e377c2',
                '#7f7f7f',
                '#bcbd22',
                '#17becf',
                '#FD3216',
                '#00FE35',
                '#6A76FC',
                '#FED4C4',
                '#FE00CE',
                '#0DF9FF',
                '#F6F926',
                '#FF9616',
                '#479B55',
                '#EEA6FB',
                '#DC587D',
                '#D626FF',
                '#6E899C',
                '#00B5F7',
                '#B68E00',
                '#C9FBE5',
                '#FF0092',
                '#22FFA7',
                '#E3EE9E',
                '#86CE00',
                '#BC7196',
                '#7E7DCD',
                '#FC6955',
                '#E48F72'
                ]

    return {
            'config':   {
                'title': {
                        'fontSize': 24,
                        'font': titleFont,
                        'anchor': 'start',
                        'fontColor': "#000000",
                        'dy': -20
                            },
                'view':{
                        'continuousWidth': 500,
                        'continuousHeight': 250,
                        },
                'axisX':    {
                        'domain': True,
                        'domainColor': axisColor,
                        'domainWidth': 1,
                        'grid': False,
                        'labelFont': labelFont,
                        'labelAngle': 0,
                        'tickColor': axisColor,
                        "tickSize": 5,
                        "titleFont": font,
                        "titleFontSize": 12,
                        "titlePadding": 10,
                        "title": "X Axis Title (units)",
                            },
                    'axisY': {
                        "domain": False,
                        "grid": True,
                        "gridColor": gridColor,
                        "gridWidth": 1,
                        "labelFont": labelFont,
                        "labelFontSize": 12,
                        "labelAngle": 0,
                        "ticks": False,
                        "titleFont": font,
                        "titleFontSize": 12,
                        "titlePadding": 10,
                        "title": "Y Axis Title (units)",
                        "titleAngle": 0,
                        "titleY": -10,
                        "titleX": -50,
                            },
                    'range': {
                        'category': plotly34
                            },
                    'mark': {
                        'fillOpacity': .5
                            }
                        }
            }


alt.themes.register('custom_irc', irc_style)
