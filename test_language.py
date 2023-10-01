""" Module to test languages. """
# standard imports
from pathlib import Path
import os

# internal imports
from interface import ProgrammingLanguage
from util import read_file

DATA_PATH = Path(os.environ["INPUT_DATAPATH"])

def test_languages():
    """Test function for programming languages."""

    for file in (DATA_PATH / "languages").iterdir():
        lang = ProgrammingLanguage.model_validate(read_file(file))
        file_name = file.name.replace(file.suffix, "")

        # Make sure file name is same as developer name
        # it can be case insensitve and ignore spaces
        assert file_name == lang.name.lower() or file_name == lang.name.lower().replace(
            " ", ""
        )
