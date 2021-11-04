"""Add the required modules for the tests."""

# Load the librairies
import os
import sys


# Add the module
path_libraries = os.path.join(os.getcwd(), "fly_me_bot")
if path_libraries not in sys.path:
    sys.path.append(path_libraries)

path_libraries = os.path.join(path_libraries, "shared_code")
if path_libraries not in sys.path:
    sys.path.append(path_libraries)
