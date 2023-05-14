from nicegui import ui
import js2py

def run_js_function(js_function):
    context = js2py.EvalJs()
    context.execute(js_function)
    return context

js_function = """
    function add(a,b){
        return a+b;
    }
"""

context = run_js_function(js_function)
result = context.add(2,3)

async def add_data():
    await ui.run_javascript(
        '''
		'''
    )
print(add_data())
ui.run(port = 8082)