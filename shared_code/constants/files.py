"""Define the constants for the files."""

# Import the libraries.
import os
from typing import Final
from dataclasses import dataclass


@dataclass(frozen=True)
class FILES:  # pylint: disable=C0103
    """Handles the constants for the files."""

    PATH_TO_DATA: Final = os.path.join(
        "C:",
        os.sep,
        "Users",
        "serge",
        "OneDrive",
        "Data Sciences",
        "Data Sciences - Ingenieur IA",
        "10e projet",
        "Deliverables",
        "data",
    )

    FRAME_RAW_DATA: Final = os.path.join(PATH_TO_DATA, "frames", "frames.json")
