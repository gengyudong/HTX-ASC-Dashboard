# from nicegui import ui
# from utils.d2_bankperformance import *
# import pymysql
# import pandas as pd

# connection = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')
# df = pd.read_sql_query("SELECT * FROM sys.scam_management_system", connection)


# bank_performance_grid(df)

# ui.run(port = 8083)


import pymysql
import pandas as pd
from nicegui import ui
connection = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')
df = pd.read_sql_query("SELECT * FROM sys.scam_management_system", connection)
df['reaction_time'] =  df['datetime_bank_account_frozen']- df['datetime_production_order_served']
groupedBank = df.groupby('account_bank')

agg_function = {'amount_scammed':['min', 'max', 'sum', 'mean'],
                'reaction_time': ['min', 'max', 'sum', 'mean'],
                'datetime_production_order_served': 'count',
                }

stats = groupedBank.agg(agg_function)
stats.columns = ['-'.join(col) for col in stats.columns.values]
banks = stats.index.to_list()


#implement a sort later

dropdown = ui.select(['avg', 'min', 'sum', 'mean'], value='mean') #later rename sum to Total


#   Bank's Performance Table

grid = ui.aggrid.from_pandas(stats).classes('max-h-40')
grid

def update():
    grid.options['rowData'][0]['age'] += 1
    grid.update()


ui.run()