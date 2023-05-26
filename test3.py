from nicegui import Client, ui
from test2 import *

@ui.page('/')
async def page(client: Client):
    
    ui.select(['min', 'max', 'sum', 'mean'], value='mean', on_change=change_stats)
    generate_grid()
    await client.connected(timeout=15.0)
    await add_handler()

ui.run()