from nicegui import ui
import pymysql
import pandas as pd
from test2 import *


connection2 = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')

cursor = connection2.cursor()
cursor.execute("SELECT UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = 'sys' AND TABLE_NAME = 'sys_config'")
result = cursor.fetchone()
initial_updated_time = result[0]


def data():
    connection2 = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')
    
    df_test = pd.read_sql_query("SELECT * FROM sys.sys_config", connection2)
    
    return df_test


@ui.refreshable
def content():
    df_test = data()
   
    chart(df_test)
    
content()

    
def check_db_change():
    cursor.execute("SELECT UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = 'sys' AND TABLE_NAME = 'sys_config'")
    result = cursor.fetchone()
    latest_update_time = result[0]
    global initial_updated_time
    global df_test
    if latest_update_time != initial_updated_time:
        content.refresh()
        initial_updated_time = latest_update_time
    

ui.timer(5.0, check_db_change)
ui.run(port = 8082)

