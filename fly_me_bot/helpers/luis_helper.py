# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Transform by Serge Neuman pf the P of OC

import logging
logger = logging.getLogger("Luis Helper")
logger.setLevel(level= logging.INFO)
logger.info("Je suis on...")


from enum import Enum
from typing import (Dict, Tuple)
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from journey_details import Journey_details

from shared_code.constants.luis_app import LUIS_APPS



def top_intent(intents: Dict[LUIS_APPS, dict]) -> TopIntent:
    """Return the top intent.

    Args:
        intents (Dict[Intent, dict]): the intents discovered by Luis

    Returns:
        TopIntent: The top intent found.
    """
    max_intent = LUIS_APPS.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    """Handle the communication with Luis."""

    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> Tuple[LUIS_APPS, object]:
        """Return an object with preformatted LUIS results for the bot's dialogs to consume."""
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            # Check that Luis has found something with enough confidence.
            if recognizer_result.intents[intent].score < LUIS_APPS.THREESHOLD_FOR_VALID_INTENT:
                intent = None


            if intent == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]:
                logger.info("Need to decode the intent.")
                result = Journey_details()

                # We need to get the result from the LUIS JSON which at every level returns an array.
                to_entities = recognizer_result.entities.get("$instance", {}).get(
                    LUIS_APPS.ENTITIES["To place name"], []
                )
                if len(to_entities) > 0:
                    if recognizer_result.entities.get(LUIS_APPS.ENTITIES["To place name"], [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.destination = to_entities[0]["text"].capitalize()
                    else:
                        result.unsupported_airports.append(
                            to_entities[0]["text"].capitalize()
                        )

                from_entities = recognizer_result.entities.get("$instance", {}).get(
                    LUIS_APPS.ENTITIES["From place name"], []
                )
                if len(from_entities) > 0:
                    if recognizer_result.entities.get(LUIS_APPS.ENTITIES["From place name"], [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.origin = from_entities[0]["text"].capitalize()
                    else:
                        result.unsupported_airports.append(
                            from_entities[0]["text"].capitalize()
                        )

                # This value will be a TIMEX. And we are only interested in a Date so grab the first result and drop
                # the Time part. TIMEX is a format that represents DateTime expressions that include some ambiguity.
                # e.g. missing a Year.
                date_entities = recognizer_result.entities.get("datetime", [])
                if date_entities:
                    timex = date_entities[0]["timex"]

                    if timex:
                        datetime = timex[0].split("T")[0]

                        result.travel_date = datetime

                else:
                    result.travel_date = None

        except Exception as exception:
            logger.info(f"Pb: {exception}")
            print(exception)

        return intent, result
