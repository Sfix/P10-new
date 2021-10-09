"""Class to read the data for LUIS and create the json to train and test."""

# Load the libriries
from typing import Dict
from typing import List
from typing import Union

import json
import pandas as pd

from shared_code.constants.files import FILES
from shared_code.constants.utterances import UTTERANCES


class Frames:
    """Read the json and create the json needed for LUIS."""

    def __init__(self) -> None:
        """Init the class."""
        self.__df_raw_data: pd.DataFrame = self.__load_raw_data()
        self.__df_utterances: pd.DataFrame = self.get_utterances()

    #
    # Private
    #
    def __load_raw_data(self) -> pd.DataFrame:
        """Load the raw data.

        Returns:
            pd.DataFrame: the json in a pandas dataframe.
        """
        with open(file=FILES.FRAME_RAW_DATA, mode="r", encoding="utf-8") as handler:
            json_raw_data = json.load(handler)
        return pd.DataFrame(data=json_raw_data)

    def __decode_raw_acts(self, acts: List) -> List:
        """Decode the turns and retrieve the Entities.

        Args:
            turn (List): A full dialog.

        Returns:
            List: The turn by turn information.
        """
        from_date = None
        to_date = None
        from_place = None
        to_place = None
        max_budget = None
        for act in acts:
            if act["name"] != "inform":
                continue
            for arg in act["args"]:
                if arg["key"] == UTTERANCES.ENTITY_FROM_PLACE_IN_FRAMES:
                    from_place = arg["val"]
                elif arg["key"] == UTTERANCES.ENTITY_TO_PLACE_IN_FRAMES:
                    to_place = arg["val"]
                elif arg["key"] == UTTERANCES.ENTITY_FROM_DATE_IN_FRAMES:
                    from_date = arg["val"]
                elif arg["key"] == UTTERANCES.ENTITY_TO_DATE_IN_FRAMES:
                    to_date = arg["val"]
                elif arg["key"] == UTTERANCES.ENTITY_MAX_BUDGET_IN_FRAMES:
                    max_budget = arg["val"]
        return {
            UTTERANCES.ENTITY_FROM_PLACE: from_place,
            UTTERANCES.ENTITY_TO_PLACE: to_place,
            UTTERANCES.ENTITY_FROM_DATE: from_date,
            UTTERANCES.ENTITY_TO_DATE: to_date,
            UTTERANCES.ENTITY_MAX_BUDGET: max_budget,
        }

    def __decode_raw_turns(self, turns: List) -> List:
        """Decode the turns and retrieve the Entities.

        Args:
            turn (List): A full dialog.

        Returns:
            List: The turn by turn information.
        """
        decoded_acts = [
            self.__decode_raw_acts(turn["labels"]["acts"])
            if turn["author"] == "user"
            else {}
            for turn in turns
        ]
        return [
            {
                "text": turns[n]["text"],
                "author": turns[n]["author"],
                UTTERANCES.ENTITY_FROM_PLACE: decoded_acts[n][
                    UTTERANCES.ENTITY_FROM_PLACE
                ],
                UTTERANCES.ENTITY_TO_PLACE: decoded_acts[n][UTTERANCES.ENTITY_TO_PLACE],
                UTTERANCES.ENTITY_FROM_DATE: decoded_acts[n][
                    UTTERANCES.ENTITY_FROM_DATE
                ],
                UTTERANCES.ENTITY_TO_DATE: decoded_acts[n][UTTERANCES.ENTITY_TO_DATE],
                UTTERANCES.ENTITY_MAX_BUDGET: decoded_acts[n][
                    UTTERANCES.ENTITY_MAX_BUDGET
                ],
            }
            for n in range(len(turns))
            if turns[n]["author"] == "user"
        ]

    def __decode_raw_data(self, row) -> Dict[str, Union[str, int, float, None]]:
        """Decode a line of Frames.

        Args:
            row (Dict): one line of the raw data.

        Returns:
            Dict[str, Union[str, int, float, None]]: Decoded row for Utterances.
        """
        rating = (
            row["labels"]["userSurveyRating"]
            if row["labels"]["wizardSurveyTaskSuccessful"]
            else -row["labels"]["userSurveyRating"]
        )
        turns = self.__decode_raw_turns(row["turns"])
        return [
            {
                "id": row["id"],
                "rating": rating,
                "text": decoded_turn["text"],
                UTTERANCES.ENTITY_FROM_PLACE: decoded_turn[
                    UTTERANCES.ENTITY_FROM_PLACE
                ],
                UTTERANCES.ENTITY_TO_PLACE: decoded_turn[UTTERANCES.ENTITY_TO_PLACE],
                UTTERANCES.ENTITY_FROM_DATE: decoded_turn[UTTERANCES.ENTITY_FROM_DATE],
                UTTERANCES.ENTITY_TO_DATE: decoded_turn[UTTERANCES.ENTITY_TO_DATE],
                UTTERANCES.ENTITY_MAX_BUDGET: decoded_turn[
                    UTTERANCES.ENTITY_MAX_BUDGET
                ],
            }
            for decoded_turn in turns
        ]

    #
    # Public
    #
    def get_utterances(self) -> pd.DataFrame:
        """Create the DataFrame of the utterances.

        Returns:
            pd.DataFrame: Dataframe with the text and the entities
        """
        decoded_raw_data = [
            element
            for value in [
                self.__decode_raw_data(row)
                for _, row in self.__df_raw_data.iterrows()
                if row["labels"]["userSurveyRating"] is not None
            ]
            for element in value
        ]
        return pd.DataFrame(decoded_raw_data)

    @property
    def df_utterances(self) -> pd.DataFrame:
        """Returns the DataFrame of utterances.

        Returns:
            pd.DataFrame: pandas dataframe of the user's utterances
        """
        return self.__df_utterances


# Element for debug
if __name__ == "__main__":
    frame = Frames()
    print(len(frame))
