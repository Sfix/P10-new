#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os

from dotenv import load_dotenv
# The notebook is not in the root of the apps. So we need to provide the path
# to the ".env"
load_dotenv(dotenv_path= '..')


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = os.getenv("MicrosoftAppId", "")
    APP_PASSWORD = os.getenv("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.getenv("LuisAppId", "")
    LUIS_API_KEY = os.getenv("LuisAPIKey", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.getenv("LuisAPIHostName", "")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.getenv(
        "AppInsightsInstrumentationKey", ""
    )
