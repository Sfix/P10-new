"""Study the Frames."""

# %% [markdown]
#

# %%
# Load the libriraries
import os
import sys
import json

from shared_code.constants.files import FILES


# %%
# Add the path to the system
path_libraries = os.path.join(os.getcwd(), "..")
if path_libraries not in sys.path:
    sys.path.append(path_libraries)


# %%
# Reas the json
with open(file=FILES.FRAME_RAW_DATA, mode="r", encoding="utf-8") as handler:
    raw_data = json.load(handler)

# %%
