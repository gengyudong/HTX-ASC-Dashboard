from nicegui import ui
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, timedelta
import plotly.graph_objects as go

#   Style
ui.add_head_html('''
    <style> 
        body {background-color : #0e1c2f};
    </style>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600&display=swap" rel="stylesheet">
    ''')

box_1_style = '''
    height: 47vh;
    width: 40%;
    
    border-style: solid; 
    border-width: 1px; 
    border-radius: 10px;
    border-color: #0E1C2F; 
    
    display: flex; 
    align-items: center;
    text-align: center;
    
    font-family: "Poppins"; 
    color: #CED5DF;
'''
box_2_style = '''
    height: 47vh;
    width: 60%;
    
    border-style: solid; 
    border-width: 1px; 
    border-radius: 10px;
    border-color: #132238; 
    
    background-color: #132238;
'''

box_3_4_style = '''
    height: 47vh;
    width: 50%;
    
    border-style: solid; 
    border-width: 1px; 
    border-radius: 10px;
    border-color: #0E1C2F; 
    
    background-color: #132238;
    
    font-family: "Poppins"; 
    color: #CED5DF;
'''

percentage_style = ('''
    min-width: 6.2vw;
    
    border-style: solid; 
    border-width: 1px; 
    border-radius: 20px;
    
    background-color: #0B403E;
    
    margin: auto;
    padding: 3px 5px 3px 3px;
    
    font-size: 0.8vw;
    font-weight: 600;
''')

ui.colors(primary='#6E93D6', secondary='#132238', accent='#111B1E', positive='#CED5DF')

# Initiating Connection with DB
connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)


with ui.row().style('width: 100%'):
    
    #   Box 1: Scam Count  
    with ui.element('div').style(box_1_style):
        
        ##   Determining figure for Scam Count
        total_victim = len(df.index)
        total_victim = '{:,}'.format(total_victim)
        total_victim_font_size = 6 - (len(str(total_victim)) - 7)//2
        
        
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
            
            ui.label('Total Reports').style('font-size: 2vw')
            
            ui.label(total_victim).style(f'font-size: {total_victim_font_size}vw; color: #E6EAEF')
            
            with ui.row():
                for i in range(4):
                    arrow_array = [day_arrow, week_arrow, month_arrow, year_arrow]
                    percentage_array = [day_percentage, week_percentage, month_percentage, year_percentage]
                    word_array = ['DoD', 'WoW', 'MoM', 'YoY']
                    
                    arrow = arrow_array[i]
                    percentage_num = percentage_array[i]
                    word = word_array[i]
                    
                    if arrow == 'arrow_upward':
                        with ui.row().classes('items-center').style(percentage_style).style('background-color: #3D1915; border-color: #3D1915'):
                            ui.icon(arrow).style('margin-left: 6px; margin-right: -10px; color: #C14A78; font-weight: 800')
                            ui.label(f'{percentage_num}% {word}').style('color: #C14A78')
                    
                    elif arrow == 'arrow_downward':
                        with ui.row().classes('items-center').style(percentage_style).style('background-color: #0B403E; border-color: #0B403E'):
                            ui.icon(arrow).style('margin-left: 6px; margin-right: -10px; color: #4AC193; font-weight: 800')
                            ui.label(f'{percentage_num}% {word}').style('color: #4AC193')
                    
                    elif arrow == 'remove':
                        with ui.row().classes('items-center').style(percentage_style).style('background-color: #404F63; border-color: #404F63'):
                            ui.icon(arrow).style('margin-left: 6px; margin-right: -5px; color: #CED5DF; font-weight: 800')
                            ui.label(f'0% {word}').style('color: #CED5DF')
                            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#             
    
    #   Box 2: Choropleth Map Plot
    with ui.element('div').style(box_2_style):
        None
        
    
    
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#             

with ui.row().style('width: 100%'):

    #   Box 3: Scam Count Plot
    
    with ui.element('div').style(box_3_4_style):
        
        with ui.row().style('padding: 2vh 0px 0px 30px; font-weight: 700; font-size: 1vw').classes('items-center'):
            
            ui.label('Scam Count')
            ui.toggle(['D', 'W', 'M', 'Y'], value = 'D').style('margin-left: 30%')
            ui.button('Filter').props('color = positive').style('margin-left: 3vw')
            
            
        ##  Getting x & y data ready
        today = date.today()
        dates = []
        no_of_cases = []

        for i in range(30):
            previous_date = today - timedelta(days = i)
            dates.append(previous_date)
        
        dates.reverse()
        
        for date in dates:
            df_for_this_date = df[df.date_assigned == date]
            no_of_cases_on_this_date = len(df_for_this_date.index)
            no_of_cases.append(no_of_cases_on_this_date)

        for date in dates:
            date = date.strftime("%#Y-%#m-%d")
        
        ##  Plotting Graph
        scam_count_bar_graph = go.Figure()
        scam_count_bar_graph.add_trace(go.Bar(
            x = dates,
            y = no_of_cases,
            marker_color = '#2C7BE5',
            opacity = 0.8
        )) 
        
        scam_count_bar_graph.update_layout(
            margin = {'l': 25, 'r': 0, 't': 30, 'b': 30},
            font = {'family': 'Poppins', 'color': '#5F7A95'},
            paper_bgcolor = '#132238',
            plot_bgcolor = '#132238'
        )
        
        scam_count_bar_graph.update_xaxes(
            showgrid = False
        )
        
        scam_count_bar_graph.update_yaxes(
            gridcolor = '#5F7A95',
            griddash = 'dot',
            zerolinecolor = '#5F7A95',
            zerolinewidth = 1
        )
        
        
        ui.plotly(scam_count_bar_graph).style('margin: auto; margin-top: 5px; width: 90%; height: 80%')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#             
      
    #   Box 4: Rate of Change Plot
    with ui.element('div').style(box_3_4_style):
        
        ui.label('Rate of Change (%)').style('padding: 2vh 0px 0px 30px; font-weight: 700; font-size: 1vw')

        ##  Getting x & y data ready
        date = dates[1:]
        
        rate_of_change = []
        
        for i in range(1, 30):
            change = 0
            old = no_of_cases[i-1]
            new = no_of_cases[i]
            if old == 0:
                rate_of_change.append(0)
            else:
                change = (new - old) / old * 100
                change = round(change, 1)
                rate_of_change.append(change)
        
        
        ##  Plotting Graph
        rate_of_change_line_graph = go.Figure()
        rate_of_change_line_graph.add_trace(go.Scatter(
            x = date,
            y = rate_of_change,
            mode = 'lines + markers',
            line = {'width': 3, 'color': '#2C7BE5'},
            
            marker_color = '#132238',
            marker = {'size': 8, 'color': '#132238', 'opacity': 1, 'line': {'color': '#2C7BE5', 'width': 2}},
            
            opacity = 0.9
        )) 
        
        rate_of_change_line_graph.update_layout(
            margin = {'l': 25, 'r': 0, 't': 30, 'b': 30},
            font = {'family': 'Poppins', 'color': '#5F7A95'},
            paper_bgcolor = '#132238',
            plot_bgcolor = '#132238'
        )
        
        rate_of_change_line_graph.update_xaxes(
            showgrid = False
        )
        
        rate_of_change_line_graph.update_yaxes(
            gridcolor = '#5F7A95',
            griddash = 'dot',
            zerolinecolor = '#5F7A95',
            zerolinewidth = 1
        )
        
        ui.plotly(rate_of_change_line_graph).style('margin: auto; margin-top: 5px; width: 90%; height: 80%')
   
 #-------------------------------------------------------------------------------------------------------------------------------------------------------------#             

  
ui.run(port = 8081)
