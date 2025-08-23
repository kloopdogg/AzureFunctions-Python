"""
# function_app.py
This is the main entry point of an Azure Functions project using Python.
It registers blueprints containing the actual functions.
"""
import azure.functions as func
from functions.blueprint_http_functions import bp_http
from functions.blueprint_timer_functions import bp_timer
from functions.blueprint_asb_functions import bp_asb

app = func.FunctionApp()
app.register_functions(bp_http)
app.register_functions(bp_timer)
app.register_functions(bp_asb)
