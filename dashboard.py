from nicegui import ui
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import date, timedelta

### Style
ui.add_head_html('''
    <style> 
        body {background-color: #F1F1F1}
    </style>
''')

percentage_style = '''
    width: 125px;
    font-size: 14px;
    border-style: solid; 
    border-width: 1px; 
    border-radius: 20px;
    border-color: FFFFFF; 
    background-color: white
'''

upward_arrow_style = '''
    margin-top: 3.2px; 
    margin-left: 10px; 
    color: #FF4D4D;
    font-weight: bold;
'''
upward_percentage_style = '''
    margin-left: -10px; 
    color: #ff4d4d; 
    font-weight: bold;
    letter-spacing: 0.5px;
'''

downward_arrow_style = '''
    margin-top: 3.2px; 
    margin-left: 10px; 
    color: #39E600;
    font-weight: bold;
'''
downward_percentage_style = '''
    margin-left: -10px; 
    color: #39E600; 
    font-weight: bold;
    letter-spacing: 0.5px;
'''

graph_style = '''
    margin: auto;
    margin-top: 30px;
    background-color: red;
    border-width: 10px;
    border-radius: 20px;
    border-color: white;
'''
#Link Data
# connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
# df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)

### Determining percentage & arrow type
total_victim = 0

today_victim = 100000
past_week_victim = 110000
past_month_victim = 70000
past_year_victim = 30000

def percentage(today, past):
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
        return None #Need to find an icon for this


week_percentage = percentage(today_victim, past_week_victim)
week_arrow = arrow_type(today_victim, past_week_victim)

month_percentage = percentage(today_victim, past_month_victim)
month_arrow = arrow_type(today_victim, past_month_victim)

year_percentage = percentage(today_victim, past_year_victim)
year_arrow = arrow_type(today_victim, past_year_victim)

### Main Figure
with ui.element('div').style('font-family: "Century Gothic"; text-align: center; margin: 10px auto'):
    ui.label("Scam Victimsssssss").style('font-size: 35px; color: #505050; letter-spacing: 2px; margin-bottom: -10px')
    ui.label('123,456').style('font-size: 100px; letter-spacing: 5px')
    
    with ui.row().style('margin-top: -5px; opacity: 0.75'):
        #Week
        with ui.row().style(percentage_style):
            if week_arrow == 'arrow_upward':
                ui.icon(week_arrow).style(upward_arrow_style)
                ui.label(str(week_percentage) + '% WoW').style(upward_percentage_style)
            elif week_arrow == 'arrow_downward':
                ui.icon(week_arrow).style(downward_arrow_style)
                ui.label(str(week_percentage) + '% WoW').style(downward_percentage_style)

        #Month
        with ui.row().style(percentage_style):
            if month_arrow == 'arrow_upward':
                ui.icon(month_arrow).style(upward_arrow_style)
                ui.label(str(month_percentage) + '% MoM').style(upward_percentage_style)
            elif month_arrow == 'arrow_downward':
                ui.icon(month_arrow).style(downward_arrow_style)
                ui.label(str(month_percentage) + '% MoM').style(downward_percentage_style)
            
        #Year
        with ui.row().style(percentage_style):
            if year_arrow == 'arrow_upward':
                ui.icon(year_arrow).style(upward_arrow_style)
                ui.label(str(year_percentage) + '% YoY').style(upward_percentage_style)
            elif year_arrow == 'arrow_downward':
                ui.icon(year_arrow).style(downward_arrow_style)
                ui.label(str(year_percentage) + '% YoY').style(downward_percentage_style)


### Graph Plot

#Data Preparation
today = date.today()
dates = []
no_of_cases = []

for i in range(30):
    previous_date = today - timedelta(days = i)
    previous_date = previous_date.strftime("%#d/%#m/%Y")
    dates.append(previous_date)

dates.reverse()

# for date in dates:
#     df_for_this_date = df[df.date_assigned == date]
#     no_of_cases_on_this_date = len(df_for_this_date.index)
#     no_of_cases.append(no_of_cases_on_this_date)


with ui.element('div').style(graph_style):
    with ui.pyplot(figsize = (15,5)):
        # x = dates
        # y = no_of_cases
        x = list(range(1,31))
        y = np.random.randint(1, 300, 30)
        z = np.random.randint(1, 100, 30)

        
        plt.bar(x,y, color = '#78a9ff')
        plt.plot(x,z, color = '#993366', marker = 'o')
        plt.legend(['Rate', 'Num_Scam'])

        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.set_axisbelow(True)
        ax.set_ylabel('No. Of Scam Cases', labelpad = 15)
        ax.yaxis.grid(True, color='#d9d9d9')

with ui.element('div').style('margin:auto'):
    with ui.row():
        ui.button('Week')
        ui.button('Month')
        ui.button('Year')   
    


ui.run()