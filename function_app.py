"""
# function_app.py
# This is the main entry point of an Azure Functions project using Python.
"""
import azure.functions as func
from sample_http_blueprint import bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
app.register_functions(bp)
