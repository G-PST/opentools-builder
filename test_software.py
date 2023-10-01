""" Module to test software. """
# standard imports
from pathlib import Path
from typing import List
import os

# internal imports
from interface import SoftwareTool, Developer, Licenses, ProgrammingLanguage
from util import read_file

DATA_PATH = Path(os.environ["INPUT_DATAPATH"])

def test_valid_software():
    """Test function for software tool."""

    for file in (DATA_PATH /"software").iterdir():
        soft = SoftwareTool.model_validate(read_file(file))
        file_name = file.name.replace(file.suffix, "")

        # Make sure file name is same as developer name
        # it can be case insensitve and ignore spaces
        assert file_name == soft.name.lower() or file_name == soft.name.lower().replace(
            " ", ""
        )


def test_valid_developers_for_software():
    """Test if software entry has valid developer names."""

    developers: List[str] = []
    for file in (DATA_PATH / "developers").iterdir():
        dev = Developer.model_validate(read_file(file))
        developers.append(dev.name.lower())

    for file in (DATA_PATH / "software").iterdir():
        soft = SoftwareTool.model_validate(read_file(file))
        if isinstance(soft.developer, str):
            assert soft.developer.lower() in developers
        else:
            assert set([el.lower() for el in soft.developer]).issubset(set(developers))


def test_valid_licenses_for_software():
    """Test if software entry has valid license names."""

    licenses: List[str] = []
    for file in (DATA_PATH / "licenses").iterdir():
        licen = Licenses.model_validate(read_file(file))
        licenses.append(licen.spdx_id.lower())

    for file in (DATA_PATH / "software").iterdir():
        soft = SoftwareTool.model_validate(read_file(file))
        if isinstance(soft.license, str):
            assert soft.license.lower() in licenses
        else:
            assert set([el.lower() for el in soft.license]).issubset(set(licenses))


def test_valid_languages_for_software():
    """Test if software entry has valid language names."""

    languages: List[str] = []
    for file in (DATA_PATH / "languages").iterdir():
        lang = ProgrammingLanguage.model_validate(read_file(file))
        languages.append(lang.name.lower())

    for file in (DATA_PATH / "software").iterdir():
        soft = SoftwareTool.model_validate(read_file(file))
        if isinstance(soft.language, str):
            assert soft.language.lower() in languages
        else:
            assert set([el.lower() for el in soft.language]).issubset(set(languages))