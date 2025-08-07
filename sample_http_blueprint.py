"""
This module defines an HTTP-triggered Azure Function using a Blueprint.
It provides a welcome message that can be personalized with a name.
It also includes a default template function that responds to HTTP requests.
"""
import logging
import azure.functions as func

bp = func.Blueprint()

@bp.route(route="WelcomeMessage", methods=["GET", "POST"]) 
def welcome_message(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP trigger function that returns a welcome message.
    If a name is provided in the query string or request body,
    it personalizes the message.
    """
    logging.info("WelcomeMessage function processing a %s request for url: %s", req.method, req.url)

    name = req.params.get('name')
    if not name:
        try:
            name = req.get_body().decode('utf-8')
        except ValueError:
            pass

    message = "Azure Functions <⚡> are awesome!"
    if name:
        message = f"{name}, {message}"

    return func.HttpResponse(message, status_code=200)
