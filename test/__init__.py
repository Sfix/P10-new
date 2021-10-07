"""Add the required modules for the tests."""

# Load the librairies
import os
import sys


# Add the module
path_libraries = os.path.join(os.getcwd(), "shared_code")
if path_libraries not in sys.path:
    sys.path.append(path_libraries)
