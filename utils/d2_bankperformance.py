import pymysql
import pandas as pd
from nicegui import ui

connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')

df = pd.read_sql_query("""SELECT report_number, account_bank, datetime_production_order_served, datetime_bank_account_frozen, amount_scammed FROM scam_management_system""", connection)

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