"""Test the bot."""

# Load the libraries
import logging

logger = logging.getLogger(name="Test recognizer")
logger.setLevel(level=logging.WARNING)
logger.info("Je suis on.")

import os
import sys
from http import HTTPStatus

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment values from .env."""
    load_dotenv(
        dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
    )


from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
)

# from botbuilder.core.integration import aiohttp_error_middleware
# from botbuilder.schema import Activity
# from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
# from botbuilder.integration.applicationinsights.aiohttp import (
#     AiohttpTelemetryProcessor,
#     bot_telemetry_middleware,
# )

path_to_bot = os.path.join(os.getcwd(), "shared_code")
if path_to_bot not in sys.path:
    sys.path.append(path_to_bot)
from shared_code.constants.luis_app import LUIS_APPS

path_to_bot = os.path.join(os.getcwd(), "fly_me_bot")
if path_to_bot not in sys.path:
    sys.path.append(path_to_bot)
# from fly_me_bot.dialogs import MainDialog, Specifying_dialog
# from fly_me_bot.bots import DialogAndWelcomeBot

# from fly_me_bot.adapter_with_error_handler import AdapterWithErrorHandler
from fly_me_bot.journey_specifier_recognizer import Journey_specifier_recognizer
from fly_me_bot.config import DefaultConfig


@pytest.fixture(autouse=True)
def test_luis_intent_GREETINGS():
    """Test the non regression of Luis on GREETINGS Intent."""
    logger.info("Test l'Intent Greetings")
    # load_dotenv(
    #     dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
    # )
    logger.info(f"App_id = {os.environ['LuisAppId']}")

    client_runtime = LUISRuntimeClient(
        endpoint="https://" + os.environ["LuisAPIHostName"],
        credentials=CognitiveServicesCredentials(os.environ["LuisAPIKey"]),
    )
    sentence = {"query": "Good afternoon!"}
    luis_response = client_runtime.prediction.resolve(
        app_id=os.environ["LuisAppId"],
        query=sentence["query"],  # "Good afternoon, Serge!"
    )
    assert (
        luis_response.top_scoring_intent.intent
        == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_GREETINGS_NAME]
    )


@pytest.fixture(autouse=True)
def test_luis_intent_HELP():
    """Test the non regression of Luis on HELP Intent."""
    logger.info("Test l'Intent Help")
    # load_dotenv(
    #     dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
    # )
    logger.info(f"App_id = {os.environ['LuisAppId']}")

    client_runtime = LUISRuntimeClient(
        endpoint="https://" + os.environ["LuisAPIHostName"],
        credentials=CognitiveServicesCredentials(os.environ["LuisAPIKey"]),
    )
    luis_response = client_runtime.prediction.resolve(
        app_id=os.environ["LuisAppId"], query="I need help"
    )
    assert (
        luis_response.top_scoring_intent.intent
        == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_HELP_NAME]
    )


@pytest.fixture(autouse=True)
def test_luis_intent_Specify_Journey():
    """Test the non regression of Luis on Specify Journey Intent."""
    logger.info("Test l'Intent Specify Journey")
    # load_dotenv(
    #     dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
    # )
    logger.info(f"App_id = {os.environ['LuisAppId']}")

    client_runtime = LUISRuntimeClient(
        endpoint="https://" + os.environ["LuisAPIHostName"],
        credentials=CognitiveServicesCredentials(os.environ["LuisAPIKey"]),
    )
    luis_response = client_runtime.prediction.resolve(
        app_id=os.environ["LuisAppId"],
        query="I want to go to Hawaï from Geneva "
        + "for 1 month starting at Christmass!"
        + " My budget is less than 5000 Euro.",
    )
    assert (
        luis_response.top_scoring_intent.intent
        == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
    )


@pytest.fixture(autouse=True)
def test_recognizer_creation():
    """Test the creation of the recognizer."""
    logger.info("Entre dans test_recognizer_creation...")
    # load_dotenv(
    #     dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
    # )
    logger.info(f"App_id = {os.environ['LuisAppId']}")

    # from fly_me_bot.config import DefaultConfig
    CONFIG = DefaultConfig()
    logger.info(f"{CONFIG.LUIS_API_KEY}")
    # Create dialogs and Bot
    RECOGNIZER = Journey_specifier_recognizer(CONFIG)
    assert RECOGNIZER.is_configured


# def test_serge():
#     from botbuilder.schema import ChannelAccount, ConversationParameters, Activity, ActivityTypes
#     from botframework.connector import ConnectorClient
#     from botframework.connector.auth import MicrosoftAppCredentials

#     CONFIG = DefaultConfig()

#     APP_ID = CONFIG.APP_ID
#     APP_PASSWORD = CONFIG.APP_PASSWORD
#     SERVICE_URL = "https://" + CONFIG.SERVICE_URL + f":{CONFIG.PORT}"
#     CHANNEL_ID = 'Serge'
#     BOT_ID = '<bot-id>'
#     RECIPIENT_ID = '<user-id>'

#     credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
#     connector = ConnectorClient(credentials, base_url=SERVICE_URL)

#     conversation = connector.conversations.create_conversation(ConversationParameters(
#                 bot=ChannelAccount(id=BOT_ID),
#                 members=[ChannelAccount(id=RECIPIENT_ID)]))

#     connector.conversations.send_to_conversation(conversation.id, Activity(
#                 type=ActivityTypes.message,
#                 channel_id=CHANNEL_ID,
#                 recipient=ChannelAccount(id=RECIPIENT_ID),
#                 from_property=ChannelAccount(id=BOT_ID),
#                 text='Hello World!'))
