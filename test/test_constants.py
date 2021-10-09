"""Test the constants."""

# Load the librairies.
import os
import logging

from shared_code.constants.files import FILES


logger = logging.getLogger("Test")
logger.setLevel(logging.INFO)


def test_constants_path_to_data():
    """Test PATH_TO_DATA."""
    assert os.path.isdir(FILES.PATH_TO_DATA)


def test_constants_frame_raw_data():
    """Test FRAME_RAW_DATA."""
    assert os.path.isfile(FILES.FRAME_RAW_DATA)
