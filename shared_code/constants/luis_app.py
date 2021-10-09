"""Define the constants for the files."""

# Import the libraries.
import os
from typing import Final
from dataclasses import dataclass

from shared_code.constants.utterances import UTTERANCES


@dataclass(frozen=True)
class LUIS_APPS:  # pylint: disable=C0103
    """Handles the constants for the LUIS App."""

    VERSION_ID: Final = "0.1"
    NAME: Final = "Fly me"
    DESCRIPTION: Final = "LUIS App for Fly me"

    INTENTS: Final = {
        "Specify journey name": "Specify journey",
        "Greetings name": "Greetings",
        "Help name": "Help",
    }

    ENTITIES: Final = {
        "From place name": UTTERANCES.ENTITY_FROM_PLACE,
        "To place name": UTTERANCES.ENTITY_TO_PLACE,
        "From date name": UTTERANCES.ENTITY_FROM_DATE,
        "To date name": UTTERANCES.ENTITY_TO_DATE,
        "Max budget": UTTERANCES.ENTITY_MAX_BUDGET,
    }

    FEATURES: Final = {
        "origin phrases list": {
            "name": "Origin words",
            "file": "words marking Origin.json",
        },
        "destination phrases list": {
            "name": "Destination words",
            "file": "words marking Destination.json",
        },
        "starting phrases list": {
            "name": "Starting words",
            "file": "words marking Start.json",
        },
        "ending phrases list": {
            "name": "Ending words",
            "file": "words marking End.json",
        },
    }
