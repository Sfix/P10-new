"""Class to read the data for LUIS and create the json to train and test."""

# Load the libriries
from typing import Dict
from typing import List
from typing import Union
from typing import Any

import os
import json
import pandas as pd

from shared_code.frames.frames import Frames
from shared_code.constants.files import FILES
from shared_code.constants.luis_app import LUIS_APPS


class Luis_app_handler:
    """Takes care of everything for the LUIS app."""

    def __init__(self) -> None:
        """Init the class."""
        self.__df_utterances: Frames = Frames()
        self.__json: json = None

    #
    # Private
    #
    def __create_json_head(self) -> json:
        """Create the head of the json for the apps.

        Returns:
            json: head of the json.
        """
        version_id = LUIS_APPS.VERSION_ID
        name = LUIS_APPS.NAME
        description = LUIS_APPS.DESCRIPTION
        return {
            "luis_schema_version": "7.0.0",
            "versionId": version_id,
            "name": name,
            "desc": description,
            "culture": "en-us",
            "tokenizerVersion": "1.0.0",
        }

    def __create_json_intents(self) -> json:
        """Create the intents part of the json for the apps.

        Returns:
            json: intents part of the json.
        """
        return {
            "intents": [
                {"name": LUIS_APPS.INTENTS["Greetings name"], "features": []},
                {
                    "name": LUIS_APPS.INTENTS["Specify Journey Name"],
                    "features": [
                        {
                            "modelName": LUIS_APPS.ENTITIES["From place name"],
                            "isRequired": False,
                        },
                        {
                            "modelName": LUIS_APPS.ENTITIES["To place name"],
                            "isRequired": False,
                        },
                        {
                            "modelName": LUIS_APPS.ENTITIES["From date name"],
                            "isRequired": False,
                        },
                        {
                            "modelName": LUIS_APPS.ENTITIES["To date name"],
                            "isRequired": False,
                        },
                        {
                            "modelName": LUIS_APPS.ENTITIES["Max budget"],
                            "isRequired": False,
                        },
                    ],
                },
                {"name": LUIS_APPS.INTENTS["Help"], "features": []},
                {"name": "None", "features": []},
            ]
        }

    def __create_json_entities(self) -> json:
        """Create the entities part of the json for the apps.

        Returns:
            json: entities part of the json.
        """
        return {
            "entities": [
                {
                    "name": LUIS_APPS.ENTITIES["From place name"],
                    "children": [],
                    "roles": [],
                    "features": [
                        {
                            "featureName": LUIS_APPS.FEATURES["origine phrases list"][
                                "name"
                            ],
                            "isRequired": False,
                        },
                        {"modelName": "geographyV2", "isRequired": False},
                    ],
                },
                {
                    "name": LUIS_APPS.ENTITIES["To place name"],
                    "children": [],
                    "roles": [],
                    "features": [
                        {
                            "featureName": LUIS_APPS.FEATURES[
                                "destination phrases list"
                            ]["name"],
                            "isRequired": False,
                        },
                        {"modelName": "geographyV2", "isRequired": False},
                    ],
                },
                {
                    "name": LUIS_APPS.ENTITIES["From date name"],
                    "children": [],
                    "roles": [],
                    "features": [
                        {
                            "featureName": LUIS_APPS.FEATURES["starting phrases list"][
                                "name"
                            ],
                            "isRequired": False,
                        },
                        {"modelName": "datetimeV2", "isRequired": False},
                    ],
                },
                {
                    "name": LUIS_APPS.ENTITIES["To date name"],
                    "children": [],
                    "roles": [],
                    "features": [
                        {
                            "featureName": LUIS_APPS.FEATURES["ending phrases list"][
                                "name"
                            ],
                            "isRequired": False,
                        },
                        {"modelName": "datetimeV2", "isRequired": False},
                    ],
                },
                {
                    "name": LUIS_APPS.ENTITIES["Max budget"],
                    "children": [],
                    "roles": [],
                    "features": [
                        {"modelName": "money", "isRequired": False},
                    ],
                },
            ]
        }

    def __create_json_hierarchicals(self) -> json:
        """Create the hierarchicals part of the json.

        Returns:
            json: hierarchicals part of the json.
        """
        return {"hierarchicals": []}

    def __create_json_composites(self) -> json:
        """Create the composites part of the json.

        Returns:
            json: composites part of the json.
        """
        return {"composites": []}

    def __create_json_closedLists(self) -> json:
        """Create the closedLists part of the json.

        Returns:
            json: closedLists part of the json.
        """
        return {"closedLists": []}

    def __create_json_prebuiltEntities(self) -> json:
        """Create the prebuiltEntities part of the json.

        Returns:
            json: prebuiltEntities part of the json.
        """
        return {
            "prebuiltEntities": [
                {"name": "datetimeV2", "roles": ["Departure", "Return"]},
                {"name": "geographyV2", "roles": ["From", "To"]},
                {"name": "money", "roles": ["Budget"]},
            ]
        }

    def __create_json_patternAnyEntities(self) -> json:
        """Create the patternAnyEntities part of the json.

        Returns:
            json: patternAnyEntities part of the json.
        """
        return {"patternAnyEntities": []}

    def __create_json_regex_entities(self) -> json:
        """Create the regex_entities part of the json.

        Returns:
            json: regex_entities part of the json.
        """
        return {"regex_entities": []}

    def __create_json_phraselists(self) -> json:
        """Create the phraselists part of the json.

        Returns:
            json: phraselists part of the json.
        """
        phrase_list_json = {"phraselists": []}
        for phrase_list in LUIS_APPS.FEATURES:
            with open(
                file=os.path.join(
                    FILES.PATH_TO_DATA, LUIS_APPS.FEATURES[phrase_list]["file"]
                ),
                mode="r",
            ) as file_handler:
                data = json.load(file_handler)
            phrase_list_json["phraselists"].append(
                {
                    "name": LUIS_APPS.FEATURES[phrase_list]["name"],
                    "mode": True,
                    "zords": f"{data['list']}",
                    "activated": True,
                    "enabledForAllModels": False,
                }
            )
        return phrase_list_json

    def __create_json_regex_features(self) -> json:
        """Create the regex_features part of the json.

        Returns:
            json: regex_features part of the json.
        """
        return {"regex_features": []}

    def __create_json_patterns(self) -> json:
        """Create the patterns part of the json.

        Returns:
            json: patterns part of the json.
        """
        return {"patterns": []}

    def __create_json_settings(self) -> json:
        """Create the settings part of the json.

        Returns:
            json: settings part of the json.
        """
        return {"settings": []}

    #
    # Public
    #
    def create_json_for_new_app(self) -> json:
        """Create the json requiered to create an Apps.

        Returns:
            json: the required json
        """
        json_app = self.__create_json_head()
        json_app.update(self.__create_json_intents())
        json_app.update(self.__create_json_entities())
        json_app.update(self.__create_json_hierarchicals())
        json_app.update(self.__create_json_composites())
        json_app.update(self.__create_json_closedLists())
        json_app.update(self.__create_json_prebuiltEntities())
        json_app.update(self.__create_json_utterances())
        json_app.update(self.__create_json_patternAnyEntities())
        json_app.update(self.__create_json_regex_entities())
        json_app.update(self.__create_json_phraselists())
        json_app.update(self.__create_json_regex_features())
        json_app.update(self.__create_json_patterns())
        json_app.update(self.__create_json_settings())
        self.__json = json_app

    @property
    def json_app(self) -> json:
        """Return the json to create the Luis.

        Returns:
            json: the json to create the Luis.
        """
        return self.__json


# Element for debug
if __name__ == "__main__":
    lah = Luis_app_handler()
    print(len(lah))
