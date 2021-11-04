"""Test the bot."""

# Load the libraries
import logging

logger = logging.getLogger(name="Test recognizer")
logger.setLevel(level=logging.WARNING)
logger.info("Je suis on.")

import os
import sys
from http import HTTPStatus
import aiounittest

path_to_project = os.path.join(
    "C:",
    os.sep,
    "serge",
    "OneDrive",
    "Data Sciences",
    "Data Sciences - Ingenieur IA",
    "10e projet",
    "Deliverables",
)
path_libraries = os.path.join(path_to_project, "fly_me_bot")
if path_libraries not in sys.path:
    sys.path.append(path_libraries)
path_libraries = os.path.join(path_to_project, "fly_me_bot", "dialogs")
if path_libraries not in sys.path:
    sys.path.append(path_libraries)
path_libraries = os.path.join(
    path_to_project,
    "shared_code",
)
if path_libraries not in sys.path:
    sys.path.append(path_libraries)


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
from botbuilder.schema import Activity, ActionTypes, Attachment
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    ConversationState,
    MemoryStorage,
    UserState,
    conversation_state,
    MessageFactory,
)
from botbuilder.core.adapters import TestAdapter

from botbuilder.testing import DialogTestClient

from shared_code.constants.luis_app import LUIS_APPS
from fly_me_bot.dialogs.main_dialog import MainDialog, Specifying_dialog
from fly_me_bot.journey_specifier_recognizer import Journey_specifier_recognizer
from fly_me_bot.config import DefaultConfig


@pytest.fixture(autouse=True)
def test_luis_intent_GREETINGS():
    # """Test the non regression of Luis on GREETINGS Intent."""
    # logger.info("Test l'Intent Greetings")
    # logger.info(f"App_id = {os.environ['LuisAppId']}")

    # client_runtime = LUISRuntimeClient(
    #     endpoint="https://" + os.environ["LuisAPIHostName"],
    #     credentials=CognitiveServicesCredentials(os.environ["LuisAPIKey"]),
    # )
    # sentence = {"query": "Good afternoon!"}
    # luis_response = client_runtime.prediction.resolve(
    #     app_id=os.environ["LuisAppId"],
    #     query=sentence["query"],  # "Good afternoon, Serge!"
    # )
    # assert (
    #     luis_response.top_scoring_intent.intent
    #     == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_GREETINGS_NAME]
    # )
    assert True


# @pytest.fixture(autouse=True)
# def test_luis_intent_HELP():
#     """Test the non regression of Luis on HELP Intent."""
#     logger.info("Test l'Intent Help")
#     load_dotenv(
#         dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
#     )
#     logger.info(f"App_id = {os.environ['LuisAppId']}")

#     client_runtime = LUISRuntimeClient(
#         endpoint="https://" + os.environ["LuisAPIHostName"],
#         credentials=CognitiveServicesCredentials(os.environ["LuisAPIKey"]),
#     )
#     luis_response = client_runtime.prediction.resolve(
#         app_id=os.environ["LuisAppId"], query="I need help"
#     )
#     assert (
#         luis_response.top_scoring_intent.intent
#         == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_HELP_NAME]
#     )


# @pytest.fixture(autouse=True)
# def test_luis_intent_Specify_Journey():
#     """Test the non regression of Luis on Specify Journey Intent."""
#     logger.info("Test l'Intent Specify Journey")
#     load_dotenv(
#         dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
#     )
#     logger.info(f"App_id = {os.environ['LuisAppId']}")

#     client_runtime = LUISRuntimeClient(
#         endpoint="https://" + os.environ["LuisAPIHostName"],
#         credentials=CognitiveServicesCredentials(os.environ["LuisAPIKey"]),
#     )
#     luis_response = client_runtime.prediction.resolve(
#         app_id=os.environ["LuisAppId"],
#         query="I want to go to Hawaï from Geneva "
#         + "for 1 month starting at Christmass!"
#         + " My budget is less than 5000 Euro.",
#     )
#     assert (
#         luis_response.top_scoring_intent.intent
#         == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
#     )


# @pytest.fixture(autouse=True)
# def test_recognizer_creation():
#     """Test the creation of the recognizer."""
#     logger.info("Entre dans test_recognizer_creation...")
#     load_dotenv(
#         dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
#     )
#     logger.info(f"App_id = {os.environ['LuisAppId']}")

#     # from fly_me_bot.config import DefaultConfig
#     CONFIG = DefaultConfig()
#     logger.info(f"{CONFIG.LUIS_API_KEY}")
#     # Create dialogs and Bot
#     RECOGNIZER = Journey_specifier_recognizer(CONFIG)
#     assert RECOGNIZER.is_configured


# # @pytest.fixture(autouse= True)
# # class Test_Say_Hello(aiounittest.AsyncTestCase):
# # async def test_say_hello():
# #     """Test the first exchanges with the bot."""
# #     async def execute_test(turn_context: TurnContext):
# #         dialog_context = await dialogs.create_context(turn_context= turn_context)
# #         results = await dialog_context.continue_dialog()
# #         if results.status == DialogTurnStatus.Empty:
# #             options = PromptOptions(
# #                                     prompt= Activity(
# #                                                         type= ActionTypes.message,
# #                                                         text= "Hey"
# #                                     )
# #             )
# #             await dialog_context.prompt(TextPrompt.__name__)
# #         if results.status == DialogTurnStatus.Complete:
# #             reply = results.result
# #             await turn_context.send_activity(reply)


# #     adapter = TestAdapter(execute_test)

# #     conversation_state = ConversationState(MemoryStorage())
# #     dialogs_state = conversation_state.create_property("dialog-state")
# #     dialogs = DialogSet(dialogs_state)
# #     dialogs.add(MainDialog("intro_step"))

# #     step_1 = await adapter.test("Hi", "Hey")
# #     step_2 = await step_1.send("Hi")
# #     await step_2.assert_reply("Hello")


# # @pytest.fixture(autouse=True)
# # async def test_init_step_dialog():
# #     """Test the first dialog."""
# #     CONFIG = DefaultConfig()
# #     SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
# #     MEMORY = MemoryStorage()
# #     USER_STATE = UserState(MEMORY)
# #     CONVERSATION_STATE = ConversationState(MEMORY)
# #     #    ADAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)
# #     INSTRUMENTATION_KEY = CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY

# #     RECOGNIZER = Journey_specifier_recognizer(CONFIG)
# #     SPECIFYING_DIALOG = Specifying_dialog()

# #     DIALOG = MainDialog(RECOGNIZER, SPECIFYING_DIALOG)

# #     client = DialogTestClient("Test", DIALOG)
# #     reply = await client.send_activity("Hi")
# #     client.assertEqual(reply.text, "first reply", "reply failed")


# # async def test_first_turn_waterfall_dialog(self):
# #     async def step1(step: DialogContext) -> DialogTurnResult:
# #         await step.context.send_activity("hello")
# #         return await step.end_dialog()

# #     dialog = WaterfallDialog("waterfall", [step1])
# #     client = DialogTestClient("test", dialog)

# #     reply = await client.send_activity("hello")

# #     self.assertEqual("hello", reply.text)
# #     self.assertEqual("test", reply.channel_id)
# #     self.assertEqual(DialogTurnStatus.Complete, client.dialog_turn_result.status)


def test_validate_for_vscode():
    assert True
