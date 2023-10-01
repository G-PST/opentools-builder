""" Entry python module for github action. """

# standard imports
import os

# third-party imports
import pytest


def main():
    """Entry function for github action."""
    try:
        data_path = os.environ["INPUT_DATAPATH"]
    except KeyError as _:
        data_path = "data"
        os.environ["INPUT_DATAPATH"] = data_path

    print(f"Data for testing: {data_path}")

    retcode = pytest.main()
    print(f"::set-output name=exitcode::{retcode}")
    assert retcode == 0


if __name__ == "__main__":
    main()