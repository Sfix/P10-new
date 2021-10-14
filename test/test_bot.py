"""Test the bot."""

# Load the libraries
import logging

logger = logging.getLogger(name="Test recognizer")
logger.setLevel(level=logging.INFO)
logger.info("Je suis on.")

import os
import sys
from http import HTTPStatus

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment values from .env."""
    load_dotenv()


from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
from botbuilder.integration.applicationinsights.aiohttp import (
    AiohttpTelemetryProcessor,
    bot_telemetry_middleware,
)

path_to_bot = os.path.join(os.getcwd(), "fly_me_bot")
if path_to_bot not in sys.path:
    sys.path.append(path_to_bot)

from fly_me_bot.dialogs import MainDialog, Specifying_dialog
from fly_me_bot.bots import DialogAndWelcomeBot

from fly_me_bot.adapter_with_error_handler import AdapterWithErrorHandler
from fly_me_bot.journey_specifier_recognizer import Journey_specifier_recognizer


@pytest.fixture(autouse=True)
def test_recognizer_creation():
    """Test the creation of the recognizer."""
    logger.info("Entre dans test_recognizer_creation...")

    from fly_me_bot.config import DefaultConfig

    CONFIG = DefaultConfig()

    # Create dialogs and Bot
    RECOGNIZER = Journey_specifier_recognizer(CONFIG)
    assert RECOGNIZER.is_configured
