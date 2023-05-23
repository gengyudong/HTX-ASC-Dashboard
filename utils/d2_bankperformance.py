import numpy as np
import pandas as pd
from nicegui import ui



### Data Processing 
def bank_performance_data(df): 
    df = df[[ 'account_bank', 'datetime_production_order_served', 
             'datetime_bank_account_frozen', 'amount_scammed']].copy()
    #   Data cleaning 
    df['account_bank'] = df['account_bank'].str.upper()

    #   Calculations
    groupedBank = df.groupby('account_bank')
    agg_function = {'amount_scammed':['min', 'max', 'sum', 'mean'],
                    'datetime_production_order_served': 'count',
                    }
    global stats 
    stats = groupedBank.agg(agg_function)
    stats.columns = ['-'.join(col) for col in stats.columns.values]
    stats = np.round(stats.reset_index(), decimals=2)

    #   Preparing Data to display
    to_display_df = stats[['account_bank', 'datetime_production_order_served-count','amount_scammed-mean']]
    to_display_df = to_display_df.rename(columns = {
                                    'account_bank': "Bank", 
                                    'datetime_production_order_served-count': 'Production Orders Sent',
                                    'amount_scammed-mean':'Amount Scammed',
                                    })
    
    return to_display_df

def bank_performance_table(df):
    ###     Grid
    grid_style = '''
        --ag-header-background-color:  #03002e;
        --ag-header-foreground-color: #CED5DF;
        
        --ag-background-color: rgb(0,0,0,0);
        --ag-foreground-color: #CED5DF;
        --ag-odd-row-background-color: #03002e;
        --ag-row-hover-color:rgb(192, 229, 249, 0.2);
    '''

    to_display_df = bank_performance_data(df)

    grid = ui.aggrid.from_pandas(to_display_df).style(grid_style)
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
                                                            'inRange']},
                                        # 'valueFormatter': (lambda x: '$'+x.data.amount_scammed-mean) #does nothing
                                            })
    # print(grid.options)


    grid.options.update(
        {'defaultColDef':{
            'sortable':True, 
            'floatingFilter': True,
            'suppressMenu' : True,
            },
        })
    grid.options.update({'rowSelection':'multiple'})
    grid.options.update({'rowMultiSelectWithClick':True})

    return grid

def change_stats(x, grid):
    for i in range(len(stats.index)):
        grid.options['rowData'][i]['Amount Scammed'] = stats['amount_scammed-'+x].iat[i]
    grid.update()

