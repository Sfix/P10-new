"""Class to read the data for LUIS and create the json to train and test."""

# Load the libriries
import json
import pandas as pd
from shared_code.constants.files import FILES


class Frames:
    """Read the json and create the json needed for LUIS."""

    def __init__(self) -> None:
        """Init the class."""
        self.__df_utterances: pd.DataFrame = self.get_utterances()

    #
    # Private
    #

    #
    # Public
    #
    def get_utterances(self) -> pd.DataFrame:
        """Create the DataFrame of the utterances.

        Returns:
            pd.DataFrame: Dataframe with the text and the entities
        """
        with open(file=FILES.FRAME_RAW_DATA, mode="r", encoding="utf-8") as handler:
            json_raw_data = json.load(handler)
