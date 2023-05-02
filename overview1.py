from nicegui import app, ui
import pymysql
import pandas as pd
from datetime import date, timedelta

from utils.d1_telco import *
from utils.d1_topscamtypes import *
from utils.d1_heatmap import *
from utils.d1_scamtypology import *
from utils.d1_heatmap import *
from d1_scamtypologytest import *

app.add_static_files('/media', 'media') 

ui.add_head_html('''            
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Michroma&display=swap" rel="stylesheet">
    ''')

general_style = '''
    border-style: solid; 
    border-width: 1px; 
    border-radius: 10px;
    border-color: rgba(28, 27, 66, 0.2); 
    
    background-color: rgba(28, 27, 66, 0.2);
    
    font-family: "Michroma"; 
    color: #CED5DF;
'''

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

scam_count_box_style =  '''
    height: 36vh; 
    width: 100%; 
    
    display: flex; 
    align-items: center;
    text-align: center;
    
    font-family: "Michroma"; 
    color: #CED5DF;
'''

percentage_style = ('''
    min-width: 6.2vw;
    
    border-style: solid; 
    border-width: 1px; 
    border-radius: 20px;
    
    margin: auto;
    padding: 3px 5px 3px 3px;
    
    font-size: 0.5vw;
    font-weight: 600;
''')

ui.video('/media/jellyfish-121604.mp4', controls = False, autoplay=True, loop=True).style(bg_video)

# Initiating Connection with DB
# connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
# df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)

connection = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')
df = pd.read_sql_query("SELECT * FROM sys.scam_management_system", connection)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

with ui.row().style('height: 50vh; width: 100%'):
    
    #   Box 1: Telco-Line Termination Chart
    with ui.element('div').style(general_style).style('height: 50vh; width: 34%'):
        telco_df = pd.read_sql_query("""select telco from scam_management_system 
        join telcos on scam_management_system.telco_report_number = telcos.report_reference """, connection)
        
        telco_plot(telco_df).style('width: 100%; height: 100%')
        
 #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
       
    with ui.column().style('height: 50vh; width: 29%'):
        
        
         #   Box 2: ASC Logo
        with ui.element('div').style('height: 10vh; width: 100%'):
            with ui.row().classes('items-center justify-center'): 
                ui.image('https://www.police.gov.sg/-/media/Spf/Archived/2021-10-28/SPF200/Homepage/Large-SPF-Logo.ashx?h=296&w=314&la=en&hash=5D66E7698CEFB5D7B9028D9905C03967').style('width: 5vw')
                ui.label('ANTI-SCAM CENTRE').style('font-family: Michroma; font-size: 1.1vw; color: #CED5DF; letter-spacing: 0.2vw; word-spacing: 0.3vw; font-weight: bold;')
            
# -------------------------------------------------------------------------------------------------------------------------------------------------------------#
      
        #   Box 3: Scam Count Figure
        with ui.element('div').style(scam_count_box_style): 
            
            ##   Determining figure for Scam Count
            df_report = df.drop_duplicates(subset=['report_number'])
            total_report = len(df_report.index)
            total_report = '{:,}'.format(total_report)
            total_report_font_size = 4 - (len(str(total_report)) - 7)//2
            
            
            ##  Determining figures for 4 percentages
            def victim_count(date):
                past_df = df[df.date_assigned == date]
                victim_count = len(past_df.index)
                
                return victim_count
            
            def percentage(today, past):
                if past == 0:
                    return 0
                
                else:
                    change = today - past
                    percentage_change = abs(change / past) * 100
                    percentage_change = round(percentage_change, 1)

                    return percentage_change

            def arrow_type(today, past):
                change = today - past
                if change > 0:
                    return 'arrow_upward'
                if change < 0:
                    return 'arrow_downward'
                else:
                    return "remove"
                
            
            ### Scam Count - Today  
            today = date.today()
            today_victim_count = victim_count(today)
            
            ### Scam Count - Past Day 
            past_day = today - timedelta(days = 1)
            past_day_victim_count = victim_count(past_day)
            
            ### Scam Count - Past Week
            past_week = today - timedelta(days = 7)
            past_week_victim_count = victim_count(past_week)
            
            ### Scam Count - Past Month
            past_month = today - timedelta(days = 30)
            past_month_victim_count = victim_count(past_month)
            
            ### Scam Count - Past Year
            past_year = today - timedelta(days = 365)
            past_year_victim_count = victim_count(past_year)
            
            ### Percentage (vs Last Day)
            day_percentage = percentage(today_victim_count, past_day_victim_count)
            day_arrow = arrow_type(today_victim_count, past_day_victim_count)
            
            ### Percentage (vs Last Week)
            week_percentage = percentage(today_victim_count, past_week_victim_count)
            week_arrow = arrow_type(today_victim_count, past_week_victim_count)

            ### Percentage (vs Last Month)
            month_percentage = percentage(today_victim_count, past_month_victim_count)
            month_arrow = arrow_type(today_victim_count, past_month_victim_count)

            ### Percentage (vs Last Year)
            year_percentage = percentage(today_victim_count, past_year_victim_count)
            year_arrow = arrow_type(today_victim_count, past_year_victim_count)
            
            with ui.element('div').style('margin: auto'):
                
                ui.label('Total Reports').style('font-size: 2vw; font-weight: 500; letter-spacing: 0.15vw; margin-top: -6vh; margin-bottom: 2vh')
                
                ui.label(total_report).style(f'font-size: {total_report_font_size}vw; color: #E6EAEF; margin-bottom: 2vh')
                
                with ui.row().style('margin-top: 1vh'):
                    for i in range(4):
                        arrow_array = [day_arrow, week_arrow, month_arrow, year_arrow]
                        percentage_array = [day_percentage, week_percentage, month_percentage, year_percentage]
                        word_array = ['DoD', 'WoW', 'MoM', 'YoY']
                        
                        arrow = arrow_array[i]
                        percentage_num = percentage_array[i]
                        word = word_array[i]
                        
                        if arrow == 'arrow_upward':
                            with ui.row().classes('items-center').style(percentage_style).style('background-color: #3D1915; border-color: #3D1915'):
                                ui.icon(arrow).style('margin-left: 6px; margin-right: -10px; color: #C14A78; font-weight: 600')
                                ui.label(f'{percentage_num}% {word}').style('color: #C14A78; letter-spacing: 0.1vw')
                        
                        elif arrow == 'arrow_downward':
                            with ui.row().classes('items-center').style(percentage_style).style('background-color: #117E73; border-color: #117E73'):
                                ui.icon(arrow).style('margin-left: 6px; margin-right: -10px; color: #28E2CF; font-weight: 600')
                                ui.label(f'{percentage_num}% {word}').style('color: #28E2CF; letter-spacing: 0.1vw')
                        
                        elif arrow == 'remove':
                            with ui.row().classes('items-center').style(percentage_style).style('background-color: #404F63; border-color: #404F63'):
                                ui.icon(arrow).style('margin-left: 6px; margin-right: -5px; color: #CED5DF; font-weight: 600')
                                ui.label(f'0% {word}').style('color: #CED5DF; letter-spacing: 0.2vw')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

    with ui.column().style('height: 50vh; width: 34%'):
        
        #   Box 5: Heatmap
        with ui.element('div').style(general_style).style('height: 50vh; width: 100%; overflow: hidden'):
            heatmap(df).style('height: 100%; width: 150%; margin: auto')
            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

with ui.row().style('height: 43vh; width: 100%'):
    
    #   Box 6: Top Scam Typologies
    with ui.element('div').style(general_style).style('height: 45vh; width: 49%'):
        top_scam_types_plot(df).style('width: 100%; height: 100%')
 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #   Box 7: Scam Typology Trend
    with ui.element('div').style(general_style).style('height: 45vh; width: 50%'):
        scam_typology_plot(df).style('height: 100%; width: 100%')
        
        
ui.run(port = 8080)