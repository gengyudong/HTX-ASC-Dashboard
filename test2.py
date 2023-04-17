import plotly
import plotly.graph_objs as go
import pandas as pd
from nicegui import ui

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

df = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv')
# Create a trace

a = df['data'].tolist()
b = df['terapia_intensiva'].tolist()

c= df['totale_positivi']

data = [go.Scatter(
    x = a,
    y = b,
)]
layout = go.Layout(
        xaxis=dict(
            title='Data',    
        ),
        yaxis=dict(
            title='Totale positivi',  
        )
    )

data1 = [go.Scatter(
        x = a,
        y = c,
    )]
    

fig = go.Figure(data=data, layout=layout)
plot = ui.plotly(fig).style('margin: auto; margin-top: 5vh; width: 90%; height: 77%')

def change_value():
    fig1 = go.Figure(data=data1, layout=layout)
    plot.update()
    
    

with ui.element('div').style(box_3_4_style):
    ui.button('W', on_click = change_value)
    

    
    

ui.run()

