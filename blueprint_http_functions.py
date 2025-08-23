"""
This module defines an HTTP-triggered Azure Function using a Blueprint.
It provides a welcome message that can be personalized with a name.
"""
import asyncio
import logging
import azure.functions as func

bp_http = func.Blueprint(http_auth_level=func.AuthLevel.FUNCTION)

@bp_http.function_name(name="WelcomeMessage")
@bp_http.route(route="WelcomeMessage", methods=["GET", "POST"]) 
async def welcome_message(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP trigger function that returns a welcome message.
    If a name is provided in the query string or request body,
    it personalizes the message.
    """
    logging.info("WelcomeMessage function processing a %s request for url: %s", req.method, req.url)

    name = req.params.get('name')
    if not name:
        body = req.get_body()
        if body:
            name = body.decode('utf-8').strip()

    message = "Azure Functions <⚡> are awesome!"
    if name:
        message = f"{name}, {message}"
    
    # Simulate some work being done
    await asyncio.sleep(0.25)

    return func.HttpResponse(message, status_code=200)
