import pandas
from nicegui import ui

def bank_performance_grid(df):
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
    
    return grid
    



