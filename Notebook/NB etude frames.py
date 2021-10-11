"""Study the Frames."""

# %% [markdown]
#

# %%
# Load the libriraries
import os
import sys
import json
from typing import Any
from typing import Dict
from typing import List

import pandas as pd

from IPython.core.display import display
from IPython.core.display import HTML

# Add the path to the system
path_libraries = os.path.join(os.getcwd(), "..")
if path_libraries not in sys.path:
    sys.path.append(path_libraries)
from shared_code.constants.files import FILES
from shared_code.constants.utterances import UTTERANCES
from shared_code.constants.luis_app import LUIS_APPS
from shared_code.frames.frames import Frames
from shared_code.luis.luis_app_handler import Luis_app_handler


# %%
# Create the Frames and the handler
data = Frames()
lui_handler = Luis_app_handler()

# %% [markdown]
# Nous regardons de plus près les données.

# %%
with open(file=FILES.TRAIN_JSON, mode="r") as file_handler:
    json_train = json.load(file_handler)
utterances = json_train["utterances"]
utterances = [
    utterance
    for utterance in utterances
    if utterance["intent"] == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
]

# %%
# Display the utterances with colors
colors = {
    UTTERANCES.ENTITY_FROM_PLACE: "Blue",
    UTTERANCES.ENTITY_TO_PLACE: "BlueViolet",
    UTTERANCES.ENTITY_FROM_DATE: "Crimson",
    UTTERANCES.ENTITY_TO_DATE: "Brown",
    UTTERANCES.ENTITY_MAX_BUDGET: "DarkGreen",
}


def display_utterances(utterances: List) -> None:
    """Display the utterances.

    Args:
        utterances (List): List of utterances
    """
    for values in utterances:
        text = values["text"]
        df_entities = pd.DataFrame(values["entities"])
        if len(df_entities) == 0:
            print(text)
        else:
            current_start_pos = 0
            html_text = ""
            for index in df_entities.sort_values(by="startPos").index:
                html_text += (
                    f"{text[current_start_pos:df_entities.loc[index, 'startPos']]}"
                )
                html_text += f"<span style=\"background-color:{colors[df_entities.loc[index, 'entity']]}\">"
                html_text += f"{text[df_entities.loc[index, 'startPos']:df_entities.loc[index, 'endPos']]}"
                html_text += "</span>"
                current_start_pos = df_entities.loc[index, "endPos"]
            html_text += text[current_start_pos:]
            display(HTML(html_text))


display_utterances(utterances)

# %%
# and for test
test_utterances = lui_handler.get_test_set(
    total=5,
    want_origin=False,
    want_destination=False,
    want_starting=False,
    want_ending=False,
    want_budget=False,
    must_be_new=False,
)
display_utterances(
    [
        utterance
        for utterance in test_utterances
        if utterance["intent"]
        == LUIS_APPS.INTENTS[LUIS_APPS.INTENT_SPECIFY_JOURNEY_NAME]
    ]
)
# %%
