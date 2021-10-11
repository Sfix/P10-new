"""Define the constants for the files."""

# Import the libraries.
import os
from typing import Final
from typing import Dict
from dataclasses import dataclass
from dataclasses import field

from shared_code.constants.utterances import UTTERANCES
from shared_code.constants.files import FILES


class LUIS_APPS:  # pylint: disable=C0103
    """Handles the constants for the LUIS App."""

    VERSION_ID: Final = "0.1"
    NAME: Final = "Fly me"
    DESCRIPTION: Final = "LUIS App for Fly me"

    INTENTS: Final[Dict[str, str]] = {
        "Specify journey name": "Specify journey",
        "Greetings name": "Greetings",
        "Help name": "Help",
    }

    ENTITIES: Final[Dict[str, str]] = {
        "From place name": UTTERANCES.ENTITY_FROM_PLACE,
        "To place name": UTTERANCES.ENTITY_TO_PLACE,
        "From date name": UTTERANCES.ENTITY_FROM_DATE,
        "To date name": UTTERANCES.ENTITY_TO_DATE,
        "Max budget": UTTERANCES.ENTITY_MAX_BUDGET,
    }

    FEATURES: Final[Dict[str, Dict[str, str]]] = {
        "origin phrases list": {
            "name": "Origin words",
            "file": FILES.WORDS_MAKING_ORIGIN,
        },
        "destination phrases list": {
            "name": "Destination words",
            "file": FILES.WORDS_MAKING_DESTINATION,
        },
        "starting phrases list": {
            "name": "Starting words",
            "file": FILES.WORDS_MAKING_START,
        },
        "ending phrases list": {
            "name": "Ending words",
            "file": FILES.WORDS_MAKING_END,
        },
    }
