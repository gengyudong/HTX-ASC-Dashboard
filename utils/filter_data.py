import pandas as pd
import os
from dotenv import dotenv_values
def filter_data(df):
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #depends on where .env file is 
    env_path = os.path.join(parent_dir, '.env')
    env_vars = dotenv_values(env_path)

    options = []
    conditionexists = False
    for key in env_vars.keys():
        if env_vars[key] == '1':
            value = key.split("_")[1].replace(".", " ")
            options.append(value)
            if key.startswith("OVERSEASLOCAL_"):
                condition = "overseas_local"
            elif key.startswith("SCAMTYPE_"):
                condition = "scam_type"
            conditionexists = True
    
    if conditionexists:
        filtered_df = df.loc[df[condition].isin(options)]
    else: 
        filtered_df = df
    
    return filtered_df
