"""
This module defines an HTTP-triggered Azure Function using a Blueprint.
It provides a welcome message that can be personalized with a name.
"""
import asyncio
import logging
import uuid
import azure.functions as func

bp_http = func.Blueprint(http_auth_level=func.AuthLevel.FUNCTION)

_MAX_BODY_BYTES = 1024

@bp_http.function_name(name="WelcomeMessage")
@bp_http.route(route="WelcomeMessage", methods=["GET", "POST"])
async def welcome_message(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP trigger function that returns a welcome message.
    If a name is provided in the query string or request body,
    it personalizes the message.
    """
    correlation_id = str(uuid.uuid4())[:8]
    logging.info("[%s] WelcomeMessage function processing a %s request for url: %s",
                 correlation_id, req.method, req.url)

    name = req.params.get('name')
    if not name:
        body = req.get_body() or b""
        if len(body) > _MAX_BODY_BYTES:
            return func.HttpResponse("Request body too large", status_code=400,
                                     mimetype="text/plain")
        if body:
            try:
                name = body.decode('utf-8').strip()
            except UnicodeDecodeError:
                return func.HttpResponse("Invalid request body encoding", status_code=400,
                                         mimetype="text/plain")

    message = "Azure Functions <⚡> are awesome!"
    if name:
        message = f"{name}, {message}"

    # Simulate some work being done
    await asyncio.sleep(0.25)

    return func.HttpResponse(message, status_code=200, mimetype="text/plain")
