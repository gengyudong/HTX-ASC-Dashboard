from nicegui import ui
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, timedelta
import plotly.graph_objects as go
from chart_studio import plotly as py
from plotly.graph_objs import *

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
    
    overflow: hidden;
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

ui.colors(primary='#183763', secondary='#132238', accent='#0E1C2F', positive='#CED5DF', info='#5F7A95')

# Initiating Connection with DB
connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)

# connection = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')
# df = pd.read_sql_query("SELECT * FROM sys.sys_config", connection)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

with ui.left_drawer().style('background-color: #0e1c2f').props('width=250'):        
    with ui.column():
        with ui.element('div').style('margin: auto; font-family: Poppins'):
            with ui.column(): 
                with ui.row().classes('items-center').style('padding-bottom: 10px'):        
                    ui.image('https://www.police.gov.sg/-/media/Spf/Archived/2021-10-28/SPF200/Homepage/Large-SPF-Logo.ashx?h=296&w=314&la=en&hash=5D66E7698CEFB5D7B9028D9905C03967').style('width: 7vw; height: auto; margin: auto')
                    ui.label('ANTI-SCAM CENTRE').style('font-family: Poppins; font-size: 1.1vw; color: #CED5DF; font-weight: bold')
                ui.button('Scam Cases', on_click = lambda: ui.open('http://127.0.0.1:8081')).props('unelevated color = accent no-caps = True').style('font-size: 1vw')
                ui.button('Losses Prevented', on_click = lambda: ui.open('http://127.0.0.1:8082')).props('unelevated color = accent no-caps = True').style('font-size: 1vw')
                ui.button('Banks', on_click = lambda: ui.open('http://127.0.0.1:8083')).props('unelevated color = accent no-caps = True').style('font-size: 1vw')
                ui.button('Scam Trends', on_click = lambda: ui.open('http://127.0.0.1:8084')).props('unelevated color = accent no-caps = True').style('font-size: 1vw')
                ui.button('Accounts Frozen', on_click = lambda: ui.open('http://127.0.0.1:8085')).props('unelevated color = accent no-caps = True').style('font-size: 1vw')
                ui.button('Monthly Statistics', on_click = lambda: ui.open('http://127.0.0.1:8086')).props('unelevated color = accent no-caps = True').style('font-size: 1vw')
                ui.button('Performance', on_click = lambda: ui.open('http://127.0.0.1:8087')).props('unelevated color = accent no-caps = True').style('font-size: 1vw')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#             

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
            
            ui.label('Total Reports').style('font-size: 2vw; font-weight: 700')
            
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
        
        #   Data Cleaning
        df_division = df[['division_assigned']].copy()
        df_division.dropna(subset = ['division_assigned'], inplace = True)
        df_division = df_division[df_division.division_assigned != '-']
        df_division = df_division.apply(lambda x: x.str.upper() if x.dtype == "object" else x)

        values_to_be_replaced = ['CAD', 'ASCOM', 'CID']
        for value in values_to_be_replaced:
            df_division = df_division.replace('.*{}.*'.format(value), value, regex=True)
        df_division = df_division.replace(['ASCOM', 'ASD', 'CID', 'TCIB', 'UMSF', 'ICB', 'APD', 'ACB', 'GOIS'], 'A')
        
        df_division = df_division.groupby('division_assigned').size().reset_index(name = 'No_of_cases_per_division')
        df_division = df_division.drop(index = [0,4,5,7,9,12,13,15,16,17,18,19]) #  How to replace the values/group them together as some are vv stubborn
        df_division = df_division.sort_values('No_of_cases_per_division', ascending = False)
        df_division = df_division.reset_index(drop = True)

        df_latlong = pd.DataFrame({'division_assigned': ['F', 'G', 'J', 'A', 'L', 'E', 'D', 'CAD'],
                                'latitude': ['1.3849575528196754', '1.3328211729396362', '1.3511672381459414', '1.2787649220017296', '1.4334351610154739', '1.3130793731128103', '1.3173533926882381', '1.278724700500034'],
                                'longitude': ['103.84533643093292', '103.93718201189469', '103.7023869984011', '103.8397629560721', '103.77890231189434', '103.8467156436066', '103.76671172354014', '103.8393872523757'],
                                'name': ['Ang Mo Kio Police Division HQ', 'Bedok Police Division HQ', 'Jurong Police Division HQ', 'Central Police Division HQ', 'Woodlands Police Division HQ', 'Tanglin Police Division HQ', 'Clementi Police Division HQ', 'Commercial Affairs Department']})
        df_division = pd.merge(df_division, df_latlong, on = 'division_assigned')

        lat_list = df_division['latitude'].tolist()
        long_list = df_division['longitude'].tolist()
        hq_list = df_division['name'].tolist()
        scam_count_list = df_division['No_of_cases_per_division'].tolist()
        
        # mapbox_access_token = 'pk.eyJ1IjoiZ2VuZ3l1ZG9uZyIsImEiOiJjbGdkcnhocXoxdzFwM2RvNnB3YmU0dm51In0.t_EXRVIhGE46Fq-3nnq_Uw'
        
        #   Plotting Scattermapbox
        heatmap = go.Figure()
        heatmap.add_trace(go.Scattermapbox(
            lat = lat_list,
            lon = long_list,
            mode = 'markers',
  
            marker = go.scattermapbox.Marker(
                autocolorscale = False,
                cauto = True,
                cmin = 0,
                # colorscale = [[0, "#fff5f0"], [0.125, "#fee0d2"], [0.25, "#fcbba1"], [0.375, "#fc9272"], [0.5, "#fb6a4a"], [0.625, "#ef3b2c"], [0.75, "#cb181d"], [1, "#67000d"]],
                colorscale = [[0, "#BBD3F2"], [0.125, "#95B5DE"], [0.25, "#6E96CA"], [0.375, "#5B87C0"], [0.5, "#4777B6"], [0.625, "#3468AC"], [0.75, "#2A60A7"], [1, "#2058A2"]],    
                color = scam_count_list,
                
                size = scam_count_list,
                sizeref = 3,
                sizemode = 'area'
            ), 
            
            text = [hq_list[i] + '<br>' + 'Scam Cases: ' + str('{:,}'.format(scam_count_list[i])) for i in range(len(hq_list))],
            hoverinfo = 'text',    
        )) 

        heatmap.update_layout(
            margin = {'l': 0, 'r': 0, 't': 0, 'b': 0},
            autosize = True, 
            mapbox = dict(
                # accesstoken = mapbox_access_token,
                center = dict(
                    lat = 1.3485143093190572,
                    lon = 103.83056220992818,
                ),
                pitch = 0,
                zoom = 10,
                style = 'light'
            ),
        )

        heatmap.update_traces(
            hoverlabel = dict(
                font = {'family': 'Poppins'}
            )
        )

        ui.plotly(heatmap).style('margin: auto; width: 100%; height: 110%; border-radius: 10px')
        
    
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#             

with ui.row().style('width: 100%'):

    #   Box 3: Scam Count Plot
    
    with ui.element('div').style(box_3_4_style):
       
        ##  Getting x & y data ready
        
        ### Getting 'day - scam count' data
        by_day = pd.Series(df['date_assigned']).value_counts().sort_index()
        df_day = by_day.rename_axis('date').reset_index(name = 'no_of_cases_per_day')

        days = df_day['date'].tolist()
        no_of_cases_day = df_day['no_of_cases_per_day'].tolist() 
        
        ### Getting 'week - scam count' data
        df_day['date'] = pd.to_datetime(df_day['date']) - pd.to_timedelta(7, unit='d')
        df_week = df_day.groupby([pd.Grouper(key='date', freq='W')])['no_of_cases_per_day'].sum().reset_index(name = 'no_of_cases_per_week')
        
        df_week['date'] = df_week['date'].dt.strftime('%Y-%m-%d')
        
        weeks = df_week['date'].tolist()
        no_of_cases_week = df_week['no_of_cases_per_week'].tolist()
        

        
        ##  Plotting Graph
        scam_count_bar_graph = go.Figure()
        scam_count_bar_graph.add_trace(go.Bar(
            x = days,
            y = no_of_cases_day,
            
            marker_color = '#2C7BE5',
            marker_line_color = '#2C7BE5',
            opacity = 0.8,
        )) 
        
        scam_count_bar_graph.update_layout(
            margin = {'l': 0, 'r': 0, 't': 100, 'b': 0},
            
            paper_bgcolor = '#132238',
            plot_bgcolor = '#132238',
            bargap = 0.5,
            font = {'family': 'Poppins', 'color': '#5F7A95'},
            
            title = {
                'text': '<b>Scam Counts<b>',
                'font': {'family': 'Poppins', 'color': '#CED5DF', 'size': 20},
                'x': 0,
                
                },
            
            updatemenus = [
                dict(
                    type = 'buttons',
                    direction = 'right',
                    active = 0,
                    
                    x = 0.9,
                    y = 1.3,
                    bgcolor = '#132238',
                    bordercolor = '#132238',
                    font = {'color': '#CED5DF', 'size': 15},
                    buttons = list(
                        [dict(
                                label = '<b> D <b>',
                                method = 'update',
                                args = [{
                                    'x': [days],
                                    'y': [no_of_cases_day]
                                }]
                        ),
                            dict(
                                label = '<b> W <b>',
                                method = 'update',
                                args = [{
                                    'x': [weeks],
                                    'y': [no_of_cases_week]
                                }]
                        ),
                            dict(
                                label = '<b> M <b>',
                                method = 'update',
                                args = [{
                                    'x': [],
                                    'y': []
                                }]
                        ),]
                    )
                )
            ]
        )
        
        scam_count_bar_graph.update_xaxes(
            showgrid = False,
            rangeslider = {'visible': True},
            rangeselector = dict(
                    activecolor = '#183763',
                    bgcolor = '#132238',
                    bordercolor = '#CED5DF',
                    borderwidth = 1,
                    font = {'color': '#E6EAEF', 'size': 13},

          
                    
                    buttons = list([
                        dict(count = 1,
                            label = "1M",
                            step = "month",
                            stepmode = "backward"),
                        dict(count = 6,
                            label = "6M",
                            step = "month",
                            stepmode = "backward"),
                        dict(count = 1,
                            label = "YTD",
                            step = "year",
                            stepmode = "todate"),
                        dict(count = 1,
                            label = "1Y",
                            step = "year",
                            stepmode = "backward"),
                        dict(label = "All",
                             step = "all")
                    ])
                ),
                range = [date.today() - timedelta(days = 30), date.today()],
                type = 'date',
        )
        
        scam_count_bar_graph.update_yaxes(
            gridcolor = '#5F7A95',
            griddash = 'dot',
            zerolinecolor = '#5F7A95',
            zerolinewidth = 1,
            
            fixedrange = False,
        )
        
        
        ui.plotly(scam_count_bar_graph).style('margin: auto; width: 90%; height: 90%')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#             
      
    #   Box 4: Rate of Change Plot
    with ui.element('div').style(box_3_4_style):
        
        ui.label('Rate of Change (%)').style('padding: 2vh 0px 0px 30px; font-weight: 700; font-size: 1vw')
        
        ##  Getting x & y data ready
        
        ### Getting 'day - rate of change' data
        days = days[1:]
        rate_of_change = []
        
        for i in range(1, len(days)+1):
            change = 0
            old = no_of_cases_day[i-1]
            new = no_of_cases_day[i]
            if old == 0:
                rate_of_change.append(0)
            else:
                change = (new - old) / old * 100
                change = round(change, 1)
                rate_of_change.append(change)
        
        
        ##  Plotting Graph
        rate_of_change_line_graph = go.Figure()
        rate_of_change_line_graph.add_trace(go.Scatter(
            x = days,
            y = rate_of_change,
            mode = 'lines + markers',
            line = {'width': 3, 'color': '#2C7BE5'},
            
            marker_color = '#132238',
            marker = {'size': 4.5, 'color': '#132238', 'opacity': 1, 'line': {'color': '#2C7BE5', 'width': 1.5}},
            
            opacity = 0.9
        )) 
        
        rate_of_change_line_graph.update_layout(
            margin = {'l': 0, 'r': 0, 't': 0, 'b': 0},
            font = {'family': 'Poppins', 'color': '#5F7A95'},
            paper_bgcolor = '#132238',
            plot_bgcolor = '#132238',
            xaxis = {
                'rangeselector': dict(
                    activecolor = '#183763',
                    bgcolor = '#132238',
                    bordercolor = '#CED5DF',
                    borderwidth = 1,
                    font = {'color': '#E6EAEF', 'size': 13},
             
                    yanchor = 'top',
                    y = 1.2,
                    buttons=list([
                        dict(count=1,
                            label="1M",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6M",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1Y",
                            step="year",
                            stepmode="backward"),
                        dict(label = "All",
                             step="all")
                    ])
                ),
                'range': [date.today() - timedelta(days = 30), date.today()]
            },
        )
        
        rate_of_change_line_graph.update_xaxes(
            showgrid = False,
            rangeslider = {'visible': True},
        )
        
        rate_of_change_line_graph.update_yaxes(
            gridcolor = '#5F7A95',
            griddash = 'dot',
            zerolinecolor = '#5F7A95',
            zerolinewidth = 1,
            fixedrange = False,
            range = [-105, 405],
        )
        
        
        ui.plotly(rate_of_change_line_graph).style('margin: auto; margin-top: 3vh; width: 90%; height: 77%')
   
 #-------------------------------------------------------------------------------------------------------------------------------------------------------------#             

  
  
  
ui.run(port = 8081)