from nicegui import ui 
import pandas as pd     

def generate_grid():
    df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    global grid
    grid = ui.aggrid.from_pandas(df)
    grid.options['rowSelection'] = 'multiple'
    grid.options['rowMultiSelectWithClick'] = True

    grid.update()

    return grid 

async def add_handler():
    await ui.run_javascript("""const grid = getElement("""+str(grid.id)+""");
        grid.gridOptions.onSelectionChanged = function(event) {
            console.log('Hello')
        }""", respond=False)

async def change_stats(event):
    print(event.value)
    grid.options['rowData'][0]['col1'] = 45
    grid.options['rowData'][1]['col1'] = 33
    grid.update()
    await add_handler()
