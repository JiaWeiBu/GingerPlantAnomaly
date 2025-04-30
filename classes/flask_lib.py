# To Run this file
# You need to install Flask
# pip install Flask
# APP.run() will run the server

from flask import Flask, jsonify, Response, request
from functools import wraps
from enum import Enum, unique
from aiohttp import ClientSession
from discord import Webhook, Embed, File

# Registry for Route to Enum
@unique
class CallbackFunctionRoute(Enum):
    """
    Enum class for registering routes to callback functions.

    Attributes:
    - ApiService: Route for the API service.
    - Index: Route for the index page.
    - Test: Route for testing purposes.
    - Train: Route for training models.
    - Predict: Route for making predictions.
    - PredictSetup: Route for setting up prediction configurations.

    Example:
    >>> CALLBACK_FUNCTION_ROUTE["ApiService"]
    '/api'
    """
    ApiService = "/api"
    Index = "/"
    Test = "/test"
    Train = "/train"
    Predict = "/predict"
    PredictSetup = "/predict_setup"

# Dictionary mapping function names to routes
CALLBACK_FUNCTION_ROUTE: dict[str, str] = {i.name: i.value for i in CallbackFunctionRoute}

# Flask application instance
APP: Flask = Flask(__name__, template_folder="templates")

# Decorators for registering routes
def Callback(func):
    """
    Generic decorator for registering a route to a callback function.

    Args:
    - func: The function to be registered.

    Returns:
    - Wrapper function that registers the route.

    Example:
    >>> @Callback
    >>> def ApiService():
    >>>     return jsonify({"message": "API Service"})
    """
    @APP.route(CALLBACK_FUNCTION_ROUTE[func.__name__])
    @wraps(func)
    def Wrapper(*args: any, **kwargs: any):
        return APP.ensure_sync(func)(*args, **kwargs)
    return Wrapper

def Get(func):
    """
    Decorator for registering a GET route.

    Args:
    - func: The function to be registered.

    Returns:
    - Wrapper function that registers the GET route.

    Example:
    >>> @Get
    >>> def Index():
    >>>     return "Hello World"
    """
    @APP.route(CALLBACK_FUNCTION_ROUTE[func.__name__], methods=["GET"])
    @wraps(func)
    def Wrapper(*args: any, **kwargs: any):
        return APP.ensure_sync(func)(*args, **kwargs)
    return Wrapper

def Post(func):
    """
    Decorator for registering a POST route.

    Args:
    - func: The function to be registered.

    Returns:
    - Wrapper function that registers the POST route.

    Example:
    >>> @Post
    >>> def Train():
    >>>     return "Training started"
    """
    @APP.route(CALLBACK_FUNCTION_ROUTE[func.__name__], methods=["POST"])
    @wraps(func)
    def Wrapper(*args: any, **kwargs: any):
        return APP.ensure_sync(func)(*args, **kwargs)
    return Wrapper

def GetPost(func):
    """
    Decorator for registering both GET and POST routes.

    Args:
    - func: The function to be registered.

    Returns:
    - Wrapper function that registers both GET and POST routes.

    Example:
    >>> @GetPost
    >>> def Predict():
    >>>     return "Prediction endpoint"
    """
    @APP.route(CALLBACK_FUNCTION_ROUTE[func.__name__], methods=["GET", "POST"])
    @wraps(func)
    def Wrapper(*args: any, **kwargs: any):
        return APP.ensure_sync(func)(*args, **kwargs)
    return Wrapper

# Example usage of the decorators
@Get
def ApiService() -> Response:
    """
    Example function registered with the Get decorator.

    This is a critical function that serves as the API service endpoint.
    Do not modify this function without understanding its implications.
    It is used to handle incoming requests and provide responses.

    Returns:
    - JSON response with the registered routes.

    Example:
    >>> curl http://localhost:5000/api
    """
    return jsonify(CALLBACK_FUNCTION_ROUTE)