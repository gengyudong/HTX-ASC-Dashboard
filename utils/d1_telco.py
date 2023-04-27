import pymysql
import pandas as pd
from nicegui import ui
connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')

#   Data Processing
telco_df = pd.read_sql_query("""select telco from scam_management_system 
join telcos on scam_management_system.telco_report_number = telcos.report_reference """, connection)

telco_count_series = telco_df.groupby('telco').size()
telco_name_list = telco_count_series.index.to_list()
telco_count_list = telco_count_series.to_list()


#   Chart
chart = ui.chart({
        'title': {
            'enabled': True,
            'text': 'Telco Line Termination Chart',
        },
        'chart': {'type': 'bar'},
        'xAxis': {'categories': telco_name_list},
        'series': [{'data': telco_count_list,
                   'dataLabels':{
                        'enabled': True
                   }
                   }],
        'legend':{
            'enabled': False
        }
    }).classes('w-full h-64')

ui.run()