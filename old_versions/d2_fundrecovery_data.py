import pandas as pd
from dotenv import dotenv_values
import os

def fund_recovery_data(df):
    df_amount_recovery = df[['amount_scammed', 'latest_balance_seized']].copy()
    df_amount_recovery = df_amount_recovery.fillna(0)
            
    amount_scammed = 0
    for i in range(len(df_amount_recovery.index)):
        amount_scammed += df_amount_recovery['amount_scammed'][i]
        
    amount_recover= 0
    for i in range(len(df_amount_recovery.index)):
        if df_amount_recovery['latest_balance_seized'][i] >= df_amount_recovery['amount_scammed'][i]:
            amount_recover += df_amount_recovery['amount_scammed'][i]
        
        else:
            amount_recover += df_amount_recovery['latest_balance_seized'][i]

    amount_recover = round(amount_recover, 2)
    amount_scammed = round(amount_scammed, 2)

    amount_recover_percentage = amount_recover / amount_scammed * 100
    amount_recover_percentage = round(amount_recover_percentage, 1)
    amount_scammed_percentage = 100.0 - amount_recover_percentage

    return amount_scammed, amount_recover, amount_recover_percentage, amount_scammed_percentage