""" Entry python module for github action. """

# standard imports
import os

from portaldata import PortalData
from sitegenerator import generate_site

def main():
    """Entry function for github action."""
    try:
        data_path = os.environ["INPUT_DATAPATH"]
    except KeyError as _:
        data_path = "data"
        os.environ["INPUT_DATAPATH"] = data_path

    print(f"Data for testing: {data_path}")

    data = PortalData(data_path)
    generate_site(data)


if __name__ == "__main__":
    main()
