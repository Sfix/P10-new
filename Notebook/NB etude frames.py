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

# Add the path to the system
path_libraries = os.path.join(os.getcwd(), "..")
if path_libraries not in sys.path:
    sys.path.append(path_libraries)
from shared_code.constants.files import FILES
from shared_code.frames.frames import Frames


# %%
# Read the json
with open(file=FILES.FRAME_RAW_DATA, mode="r", encoding="utf-8") as handler:
    raw_data = json.load(handler)
df_raw = pd.DataFrame(raw_data)

# %% [markdown]
# Decode

# %%
frame = Frames()
df_utterances = frame.df_utterances
