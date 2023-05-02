import pymysql
import pandas as pd
from nicegui import ui

connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')

### Data Processing 

df = pd.read_sql_query("""SELECT account_bank, datetime_production_order_served, datetime_bank_account_frozen, amount_scammed
FROM scam_management_system order by account_bank asc""", connection)

#   Data cleaning 
df['account_bank'] = df['account_bank'].str.upper()

#   Calculations
groupedBank = df.groupby('account_bank')
agg_function = {'amount_scammed':['min', 'max', 'sum', 'mean'],
                'datetime_production_order_served': 'count',
                }
stats = groupedBank.agg(agg_function)
stats.columns = ['-'.join(col) for col in stats.columns.values]
stats = stats.reset_index()

#   Preparing Data to display
to_display_df = stats[['account_bank', 'datetime_production_order_served-count','amount_scammed-mean']].round(2)
to_display_df = to_display_df.rename(columns = {'Account_bank': "Bank", 
                                'datetime_production_order_served-count': 'Number of Production Orders Sent',
                                'amount_scammed-mean':'Amount Scammed',
                                })

###     Grid
grid = ui.aggrid.from_pandas(to_display_df).classes('max-h-70')
grid.options['columnDefs'][0].update({'filter':'agTextColumnFilter'})
grid.options['columnDefs'][1].update({'filter':'agNumberColumnFilter',
                                      'filterParams':{
                                          'filterOptions':['lessThan', 
                                                           'lessThanOrEqual', 
                                                           'greaterThan', 
                                                           'greaterThanOrEqual',
                                                           'inRange']}
                                      }
                                      )
grid.options['columnDefs'][2].update({'filter':'agNumberColumnFilter',
                                      'filterParams':{
                                          'filterOptions':['lessThan', 
                                                           'lessThanOrEqual', 
                                                           'greaterThan', 
                                                           'greaterThanOrEqual',
                                                           'inRange']}
                                          })
grid.options.update(
        {'defaultColDef':{
            'sortable':True, 
            'floatingFilter': True,
            'suppressMenu' : True,
        },
        })

# for column in grid.options['columnDefs']:
#     column['sortable']  = True
#     column['floatingFilter']  = True
print(grid.options)

######################
ui.aggrid

dropdown = ui.select(['min', 'max', 'sum', 'mean'], value='mean', on_change = lambda x:update(x.value))

def update(x):
    for i in range(len(stats.index)):
        grid.options['rowData'][i]['Amount Scammed'] = stats['amount_scammed-'+x][i]
    grid.update()



#   Bank's Performance Table

ui.run()