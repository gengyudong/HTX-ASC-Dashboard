from nicegui import app, ui
import pymysql
import pandas as pd

from utils.d2_fundrecovery import *
from utils.d2_recoverytypology import *
from utils.d2_fundflow import *
from utils.d2_bankperformance import *

app.add_static_files('/media', 'media')

ui.add_head_html('''
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Michroma&display=swap" rel="stylesheet">
    ''')

bg_video = '''
    width: 100vw;
    height: 100vh;
    object-fit: cover;
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: -1;
'''

recovery_progress_style = '''
    height: 34.5vh;
    width: 30%;
    
    position: absolute; 
    top: 50%; 
    left: 50%; 
    transform: translate(-50%, -50%)
'''

general_style = '''
    border-style: solid; 
    border-width: 1px; 
    border-radius: 10px;
    border-color: rgba(24, 55, 99, 0.3); 
    
    background-color: rgba(24, 55, 99, 0.3);
    
    font-family: "Michroma"; 
    color: #CED5DF;
'''

ui.video('/media/jellyfish-121604.mp4', controls = False, autoplay=True, loop=True).style(bg_video)

connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)




#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

#   Fund Recovery Progress
with ui.element('div').style(recovery_progress_style):
        fund_recovery_plot(df).style('height: 100%; width: 100%; margin:auto')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

with ui.row().style('height: 65.5vh; width: 100%'):
    
    #   Recovery by Typology Plot
    with ui.element('div').style(general_style).style('height: 65.5vh; width: 35%'):
        recovery_by_typology_plot(df).style('height: 100%; width: 100%')    
      
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #   ASC Logo
    with ui.element('div').style('height: 10vh; width: 30%'):
        with ui.row().classes('items-center justify-center'): 
            ui.image('https://www.police.gov.sg/-/media/Spf/Archived/2021-10-28/SPF200/Homepage/Large-SPF-Logo.ashx?h=296&w=314&la=en&hash=5D66E7698CEFB5D7B9028D9905C03967').style('width: 5vw')
            ui.label('ANTI-SCAM CENTRE').style('font-family: Michroma; font-size: 1.1vw; color: #CED5DF; letter-spacing: 0.2vw; word-spacing: 0.3vw; font-weight: bold;')
    
 #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
      
    #   Bank's Performance
    with ui.element('div').style(general_style).style('height: 65.5vh; width: 35%'):
        ui.label("Bank's Performance").style('text-align: center')
        bank_performance_table_dropdown(df)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
   
with ui.row().style('height: 29.5vh; width: 100%'):
    
    #   Recovery Trend Plot
    with ui.element('div').style(general_style).style('height: 29.5vh; width: 70%'):
        ui.label('Recovery Trend').style('text-align: center')
     
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #   Breakdown of Fund Flow Plot
    with ui.element('div').style(general_style).style('height: 29.5vh; width: 30%'):
        fund_flow_plot(df).style('height: 100%; width: 100%')
        
        
ui.run(port = 8082)