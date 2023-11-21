""" Entry python module for github action. """

# standard imports
import sys

from portaldata import PortalData
from sitegenerator import PortalSite

def main(data_path: str, template_path: str, site_path: str, base_url: str):
    """Entry function for github action."""

    print(f"Loading data from: {data_path}")
    data = PortalData(data_path)

    print(f"Loading site templates from: {template_path}")
    site = PortalSite(data, template_path)

    print(f"Generating site in: {site_path}")
    site.generate(baseurl=base_url, outpath=site_path)


if __name__ == "__main__":

    data_path = sys.argv[1]
    template_path = sys.argv[2]
    site_path = sys.argv[3]
    base_url = sys.argv[4]

    main(data_path, template_path, site_path, base_url)
