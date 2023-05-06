from nicegui import ui
import pandas as pd


def fund_flow_plot(df):
    ###     Data Processing 
    fundFlowDf = df[['overseas_local']]
    fundFlowCount = fundFlowDf.groupby('overseas_local').size()

    #   settling wrong entry
    fundFlowCount['L-L']+=fundFlowCount['L-l']
    fundFlowCount = fundFlowCount.drop('L-l')

    #   convert to list
    fundFlowCount.to_list()

    chart = ui.chart({
            'title': {
                'text': None,
            },
            'chart': {'type': 'bar',
                      'backgroundColor': 'rgba(0,0,0,0)',},
            'xAxis': {'categories': ['L-L', 'L-O', 'O-L', 'O-O'],
                      'labels':{
                            'style': {'color': '#CED5DF'}
                        }
                    },
            'yAxis':{
                'title': {
                    'text': 'Number of Cases',
                    'style': {
                        'color': '#CED5DF'
                    },
                },
                'labels':{
                            'style': {'color': '#CED5DF'}
                        },
                'gridLineDashStyle': 'dash',
            },
            'series': [{'data': fundFlowCount.to_list(),
                        # 'color': 'rgba(52, 181, 213, 0.7)',
                        'dataLabels':{
                            'enabled': True,
                            'style': {'color': '#CED5DF'},
                        },
                        'borderWidth':0,
                    }],
            'legend':{
                'enabled': False
            }
        }).classes('w-full h-64')
    
    return chart


