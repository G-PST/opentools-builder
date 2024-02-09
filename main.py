""" Entry python module for github action. """

# standard imports
from dataclasses import dataclass
import sys

from portaldata import PortalData
from sitegenerator import PortalSite

@dataclass
class SiteGenerationConfig:

    data_path: str
    template_path: str
    asset_path: str
    site_path: str
    error_path: str
    output_path: str
    base_url: str


def validate_and_build(config: SiteGenerationConfig):
    """Entry function for github action."""

    print(f"Loading data from: {config.data_path}")
    data = PortalData(config.data_path)

    if data.has_errors():
        print(f"Problems loading data, reporting errors in {config.error_path}")
        data.write_errormessage(config.error_path)
        return "fail"

    print(f"Loading site templates from: {config.template_path}")
    site = PortalSite(data, config.template_path, config.asset_path)

    print(f"Generating site in: {config.site_path}")
    site.generate(baseurl=config.base_url, outpath=config.site_path)

    return "pass"

if __name__ == "__main__":

    config = SiteGenerationConfig(*sys.argv[1:])
    status = validate_and_build(config)

    with open(config.output_path, 'a') as outfile:
        outfile.write(f"status={status}\n")
