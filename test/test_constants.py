"""Test the constants."""

# Load the librairies.
import os
import logging

from shared_code.constants.files import FILES


logger = logging.getLogger("Test")
logger.setLevel(logging.INFO)


def test_constants():
    """Test PATH_TO_DATA."""
    assert os.path.isdir(FILES.PATH_TO_DATA)
