"""
# function_app.py
This is the main entry point of an Azure Functions project using Python.
It registers blueprints containing the actual functions.
"""
import azure.functions as func
from blueprint_http_functions import bp

app = func.FunctionApp()
app.register_functions(bp)
