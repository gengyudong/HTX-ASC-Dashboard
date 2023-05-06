from nicegui import app, ui
import pymysql
import pandas as pd

from utils.d2_fundrecovery import *
from utils.d2_recoverytypology import *
from utils.d2_fundflow import *
from utils.d2_bankperformance import *
from utils.d2_recoverytrend import *

app.add_static_files('/media', 'media')

#has 16 px padding around nicegui-content class div 

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

div_general_style = '''
    border-style: solid; 
    border-width: 1px; 
    border-radius: 10px;
    border-color: rgba(24, 55, 99, 0.3); 
    height: 100%;

    background-color: rgba(24, 55, 99, 0.3);
    
    font-family: "Michroma"; 
    color:#CED5DF;
    text-align: center;
'''
chart_general_style = '''
    height: 90%;
    width: 100%;
'''
label_style = '''
    color:#CED5DF;
    text-align: left;
    height:5%;
    margin: 10px;

'''



ui.video('/media/jellyfish-121604.mp4', controls = False, autoplay=True, loop=True).style(bg_video)

connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

with ui.row().style('height: 60vh; width: 100%; flex-wrap: nowrap'):
    
    #   Recovery by Typology Plot
    with ui.element('div').style(div_general_style).style('width: 30%'):
        ui.label("Recovery by typology").style(label_style)
        recovery_by_typology_plot(df).style(chart_general_style)


    #   ASC Logo
    with ui.column().style('width: 40%; height:100%; flex-wrap: nowrap; gap:0rem;').classes('items-center'):
        with ui.row().classes('items-center justify-center').style('width:100%;'): 
            ui.image('https://www.police.gov.sg/-/media/Spf/Archived/2021-10-28/SPF200/Homepage/Large-SPF-Logo.ashx?h=296&w=314&la=en&hash=5D66E7698CEFB5D7B9028D9905C03967').style('width: 5vw')
            ui.label('ANTI-SCAM CENTRE').style('font-family: Michroma; font-size: 1.1vw; color: #CED5DF; letter-spacing: 0.2vw; word-spacing: 0.3vw; font-weight: bold;')

    #   Fund Recovery Progress
        with ui.element('div').classes('items-center').style('align: center; height: 100%;'):
            fund_recovery_plot(df).style(' position:relative; height: 100%')

    #   Bank's Performance
    with ui.element('div').style(div_general_style).style('width: 30%'):
        with ui.row().classes('justify-between items-center').style('flex-wrap: nowrap;'):
            ui.label("Bank's Performance").style(label_style)
            ui.select(['min', 'max', 'sum', 'mean'], value='mean', on_change = lambda x:update(x.value, grid)).style('background-color: #87c6e6 !important; border-radius:5px;').classes('px-3 w-28')
        # with ui.element('div').style('height:85%'):
        grid = bank_performance_table_dropdown(df).style('height:85%;')
            # .style('height: 50vh;') #Cant get the height correct on differnet size screens  
        
    
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
   
with ui.row().style('height: 30vh; width: 100%; flex-wrap: nowrap;'):
    
    #   Recovery Trend Plot
    with ui.element('div').style(div_general_style).style('width: 70%'):
        ui.label('Recovery Trend').style(label_style)
        recovery_trend_plot(df).style(chart_general_style)
    
    #   Breakdown of Fund Flow Plot
    with ui.element('div').style(div_general_style).style('width: 30%'):
        ui.label("Breakdown of Fund Flow").style(label_style)
        fund_flow_plot(df).style(chart_general_style)
        
        
ui.run(port = 8082)