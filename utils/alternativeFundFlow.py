#####--------------------------------------
# My idea

###     Data Processing
fundFlowDf = df[['overseas_local', 'amount_scammed', 'amount_transcated']]

groupedFundFlow = fundFlowDf.groupby('overseas_local').sum()
fundFlowSeries = groupedFundFlow['amount_scammed']+groupedFundFlow['amount_transcated']
#   settling wrong entry
fundFlowSeries['L-L']+=fundFlowSeries['L-l']
fundFlowSeries = fundFlowSeries.drop('L-l').round(2)

altchart = ui.chart({
        'title': {
            'enabled': True,
            'text': 'Breakdown of Fund Flow',
        },
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['L-L', 'L-O', 'O-L', 'O-O']},
        'series': [{'data': fundFlowSeries.to_list(),
                   'dataLabels':{
                        'enabled': True
                   }
                   }],
        'legend':{
            'enabled': False
        }
    }).classes('w-full h-64')

piechart = ui.chart({
    'title': {
            'enabled': True,
            'text': 'Breakdown of Fund Flow',
        },
    'chart': {'type': 'pie'},
    'xAxis': {'categories': ['L-L', 'L-O', 'O-L', 'O-O']},
        'series': [{'data': fundFlowSeries.to_list(),
                   }],
})

