from interface import (
    ProgrammingLanguage,
    Licenses,
    Organization,
    Developer,
    SoftwareTool,
)

from util import read_file, write_file

from pathlib import Path

def normalize(x: str):
    return x.lower().replace(" ", "")

class PortalData():

    def __init__(self, datapath: str):

        datapath = Path(datapath)

        self.load_languages(datapath)
        self.load_licenses(datapath)
        self.load_organizations(datapath)
        self.load_developers(datapath)
        self.load_tools(datapath)

    def load_languages(self, datapath: Path):

        self.languages = {}

        for file in (datapath / "languages").iterdir():

            lang = ProgrammingLanguage.model_validate(read_file(file))
            lang_id = file.name.replace(file.suffix, "")

            self.languages[lang_id] = lang

    def load_licenses(self, datapath: Path):

        self.licenses = {}

        for file in (datapath / "licenses").iterdir():

            licen = Licenses.model_validate(read_file(file))
            licen_id = file.name.replace(file.suffix, "")

            self.licenses[licen_id] = licen

    def load_organizations(self, datapath: Path):

        self.organizations = {}

        for file in (datapath / "organizations").iterdir():

            org = Organization.model_validate(read_file(file))
            org_id = file.name.replace(file.suffix, "")

            self.organizations[org_id] = org

    def load_developers(self, datapath: Path):

        self.developers = {}

        for file in (datapath / "developers").iterdir():

            dev = Developer.model_validate(read_file(file))
            dev_id = file.name.replace(file.suffix, "")

            if dev.organization:
                org_id = normalize(dev.organization)
                assert org_id in self.organizations.keys()
                dev.organization = self.organizations[org_id]

            self.developers[dev_id] = dev

    def load_tools(self, datapath: Path):

        self.tools = {}

        for file in (datapath /"software").iterdir():

            tool = SoftwareTool.model_validate(read_file(file))
            tool_id = file.name.replace(file.suffix, "")


            if isinstance(tool.language, str):
                lang_id = normalize(tool.language)
                assert lang_id in self.languages.keys()
                tool.language = [self.languages[lang_id]]

            else:
                for i, lang_id in enumerate(tool.language):
                    lang_id = normalize(lang_id)
                    assert lang_id in self.languages.keys()
                    tool.language[i] = self.languages[lang_id]

            if isinstance(tool.developer, str):
                dev_id = normalize(tool.developer)
                assert dev_id in self.developers.keys()
                tool.developer = [self.developers[dev_id]]

            else:
                for i, dev_id in enumerate(soft.developers):
                    dev_id = normalize(dev_id)
                    assert dev_id in self.developers.keys()
                    tool.developer[i] = self.developers[dev_id]

            if isinstance(tool.license, str):
                licen_id = normalize(tool.license)
                licen_id = licen_id.lower().replace(" ", "")
                assert licen_id in self.licenses.keys()
                tool.license = [self.licenses[licen_id]]

            else:
                for i, licen_id in enumerate(soft.license):
                    licen_id = normalize(licen_id)
                    assert licen_id in self.licenses.keys()
                    tool.license[i] = self.licenses[licen_id]

            self.tools[tool_id] = tool

