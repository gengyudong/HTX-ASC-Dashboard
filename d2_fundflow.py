import nicegui as ui
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
                'enabled': True,
                'text': 'Breakdown of Fund Flow',
            },
            'chart': {'type': 'bar'},
            'xAxis': {'categories': ['L-L', 'L-O', 'O-L', 'O-O']},
            'series': [{'data': fundFlowCount.to_list(),
                    'dataLabels':{
                            'enabled': True
                    }
                    }],
            'legend':{
                'enabled': False
            }
        }).classes('w-full h-64')

    return chart