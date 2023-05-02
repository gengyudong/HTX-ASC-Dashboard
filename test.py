from nicegui import ui

a = 'Hello World'
b = 'hi'

def change_value():
    global a
    a = b
    
    
ui.button('press to change value', on_click=lambda: result.set_text(b))

result = ui.label(a)

if result.text == 'hi':
    ui.label('it worked')


ui.run(port = 8082)