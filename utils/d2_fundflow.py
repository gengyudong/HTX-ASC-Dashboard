from nicegui import ui
import pandas as pd
import pymysql

#style
ui.add_head_html('''
    <style> 
        body {background-color : #0e1c2f};
    </style>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600&display=swap" rel="stylesheet">
    ''')
ui.colors(primary='#183763', secondary='#132238', accent='#0E1C2F', positive='#CED5DF', info='#5F7A95')

# Initiating Connection with DB
connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)

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

ui.run()
