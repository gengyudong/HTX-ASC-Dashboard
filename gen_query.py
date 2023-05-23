from dotenv import dotenv_values
import os



#def fundflow_data(connection):   
def fundflow_data():
    query = "SELECT overseas_local, SUM(amount_scammed), SUM(amount_transcated), COUNT(*) FROM astro.scam_management_system"
    query_keyword = 'WHERE'
    for key in env_vars.keys():
        if key.startswith("SCAMTYPE_"):
            scamtype = key.split("_")[1]
            if env_vars[key] == '1':
                query += f" {query_keyword} scam_type = '{scamtype}'"
                query_keyword = "AND" #SHOULD BE OR 
    print(query)


#def recovery_typology_data(connection):
def recovery_typology_data():
    query = f"SELECT latest_balance_seized, amount_scammed, scam_type FROM astro.scam_management_system"
    query_keyword = 'WHERE'
    for key in env_vars.keys():
        if key.startswith("OL_"):
            oltype = key.split("_")[1]
            if env_vars[key] == '1':
                query += f" {query_keyword} overseas_local = '{oltype}'"
                query_keyword = "AND" # SHOULD BE OR 
    print(query)


global env_vars
env_vars = dotenv_values('new.env')

fundflow_data()
recovery_typology_data()

