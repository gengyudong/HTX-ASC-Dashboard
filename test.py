from nicegui import ui
import pymysql
import pandas as pd
from test2 import *

@ui.refreshable
def content():
    connection2 = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')

    df_test = pd.read_sql_query("SELECT * FROM sys.sys_config", connection2)
    
    chart(df_test).style('height: 80vh; width: 100%')


content()

#   Updating of db
connection2 = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')
df_test = pd.read_sql_query("SELECT * FROM sys.sys_config", connection2)
initial_df_len = len(df_test.index)

def update():
    content.refresh()

@ui.refreshable
def check_db_change():
    # Initiating Connection with DB
    # connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
    # df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)
    df_test = pd.read_sql_query("SELECT * FROM sys.sys_config", connection2)
    final_df_len = len(df_test.index)
    print(initial_df_len)
    print(final_df_len)
    
    if final_df_len != initial_df_len:
        update()

check_db_change()

def a():
    check_db_change.refresh()

ui.timer(10.0, a)
ui.run()

