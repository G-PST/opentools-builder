""" Module to test organizations. """
# standard imports
from pathlib import Path
import os

# internal imports
from interface import Organization
from util import read_file

DATA_PATH = Path(os.environ["INPUT_DATAPATH"])

def test_organization():
    """Test function for organizations."""

    for file in (DATA_PATH / "organizations").iterdir():
        org = Organization.model_validate(read_file(file))
        file_name = file.name.replace(file.suffix, "")

        # Make sure file name is same as developer name
        # it can be case insensitve and ignore spaces
        assert file_name == org.name.lower() or file_name == org.name.lower().replace(
            " ", ""
        )
