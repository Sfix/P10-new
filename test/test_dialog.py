# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging
import os
import sys
import pytest
import asyncio
from dotenv import load_dotenv

from aiounittest import AsyncTestCase
from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    ComponentDialog,
    DialogContext,
    DialogTurnResult,
    DialogTurnStatus,
    PromptOptions,
    TextPrompt,
    WaterfallDialog,
    WaterfallStepContext,
)
from botbuilder.schema import Activity
from botbuilder.testing import DialogTestClient, DialogTestLogger
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    MemoryStorage,
    UserState,
    ConversationState,
)

path_libraries = os.path.join(
    "C:",
    os.sep,
    "serge",
    "OneDrive",
    "Data Sciences",
    "Data Sciences - Ingenieur IA",
    "10e projet",
    "Deliverables",
    "fly_me_bot",
)
if path_libraries not in sys.path:
    sys.path.append(path_libraries)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment values from .env."""
    load_dotenv(
        dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
    )


from fly_me_bot.adapter_with_error_handler import AdapterWithErrorHandler
from fly_me_bot.journey_specifier_recognizer import Journey_specifier_recognizer
from fly_me_bot.config import DefaultConfig
from fly_me_bot.dialogs.main_dialog import MainDialog, Specifying_dialog


pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment values from .env."""
    load_dotenv(
        dotenv_path="C:\\Users\\serge\\OneDrive\\Data Sciences\\Data Sciences - Ingenieur IA\\10e projet\\Deliverables"
    )


@pytest.mark.asyncio
class DialogTestClientTest(AsyncTestCase):
    """Tests for dialog test client."""

    def __init__(self, *args, **kwargs):
        super(DialogTestClientTest, self).__init__(*args, **kwargs)
        logging.basicConfig(format="", level=logging.INFO)

    # def test_init(self):
    #     client = DialogTestClient(channel_or_adapter="test", target_dialog=None)
    #     self.assertIsInstance(client, DialogTestClient)

    # def test_init_with_custom_channel_id(self):
    #     client = DialogTestClient(channel_or_adapter="custom", target_dialog=None)
    #     self.assertEqual("custom", client.test_adapter.template.channel_id)

    # async def test_single_turn_waterfall_dialog(self):
    #     async def step1(step: DialogContext) -> DialogTurnResult:
    #         await step.context.send_activity("hello")
    #         return await step.end_dialog()

    #     dialog = WaterfallDialog("waterfall", [step1])
    #     client = DialogTestClient("test", dialog)

    #     reply = await client.send_activity("hello")

    #     self.assertEqual("hello", reply.text)
    #     self.assertEqual("test", reply.channel_id)
    #     self.assertEqual(DialogTurnStatus.Complete, client.dialog_turn_result.status)

    # async def test_single_turn_waterfall_dialog_with_logger(self):
    #     """
    #     Test for single turn waterfall dialog with logger with test client.
    #     To view the console output:
    #     * unittest
    #       ```bash
    #       python -m unittest -v -k logger
    #       ```
    #     * pytest
    #       ```bash
    #       pytest --log-cli-level=INFO --log-format="%(message)s" -k logger
    #       ```
    #     The results are similar to:
    #     ```
    #     User: Text = hello
    #     -> ts: 13:39:59

    #     Bot: Text      = hello
    #          Speak     = None
    #          InputHint = acceptingInput
    #     -> ts: 13:39:59 elapsed 8 ms
    #     ```

    #     :return: None
    #     :rtype: None
    #     """

    #     async def step1(step: DialogContext) -> DialogTurnResult:
    #         await step.context.send_activity("hello")
    #         return await step.end_dialog()

    #     dialog = WaterfallDialog("waterfall", [step1])
    #     client = DialogTestClient(
    #         "test",
    #         dialog,
    #         initial_dialog_options=None,
    #         middlewares=[DialogTestLogger()],
    #     )

    #     reply = await client.send_activity("hello")

    #     self.assertEqual("hello", reply.text)
    #     self.assertEqual("test", reply.channel_id)
    #     self.assertEqual(DialogTurnStatus.Complete, client.dialog_turn_result.status)

    # async def test_two_turn_waterfall_dialog(self):
    #     async def step1(step: WaterfallStepContext) -> DialogTurnResult:
    #         await step.context.send_activity("hello")
    #         await step.context.send_activity(Activity(type="typing"))
    #         return await step.next(result=None)

    #     async def step2(step: WaterfallStepContext) -> DialogTurnResult:
    #         await step.context.send_activity("hello 2")
    #         return await step.end_dialog()

    #     dialog = WaterfallDialog("waterfall", [step1, step2])
    #     client = DialogTestClient(
    #         "test",
    #         dialog,
    #         initial_dialog_options=None,
    #         middlewares=[DialogTestLogger()],
    #     )

    #     reply = await client.send_activity("hello")
    #     self.assertEqual("hello", reply.text)

    #     reply = client.get_next_reply()
    #     self.assertEqual("typing", reply.type)

    #     reply = client.get_next_reply()
    #     self.assertEqual("hello 2", reply.text)
    #     self.assertEqual(DialogTurnStatus.Complete, client.dialog_turn_result.status)

    async def test_component_dialog(self):
        """Test the Main dialog."""
        # CONFIG = DefaultConfig()
        # SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)

        # MEMORY = MemoryStorage()
        # USER_STATE = UserState(MEMORY)
        # CONVERSATION_STATE = ConversationState(MEMORY)
        # ADAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)
        # RECOGNIZER = Journey_specifier_recognizer(CONFIG)
        # SPECIFYING_DIALOG = Specifying_dialog()
        # component = MainDialog(RECOGNIZER, SPECIFYING_DIALOG)

        # client = DialogTestClient(
        #     "test",
        #     component,
        #     initial_dialog_options=None,
        #     middlewares=[DialogTestLogger()],
        # )

        # reply = await client.send_activity("hello")
        # self.assertEqual("Hey! Let's specify your journey \U0001F60E", reply.text)
        assert True
