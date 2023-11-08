from interface import (
    ProgrammingLanguage,
    Licenses,
    Organization,
    ToolCategory,
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
        self.load_categories(datapath)
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

    def load_categories(self, datapath: Path):

        self.categories = {}

        for file in (datapath / "categories").iterdir():

            cat = ToolCategory.model_validate(read_file(file))
            cat_id = file.name.replace(file.suffix, "")

            self.categories[cat_id] = cat

        for cat in self.categories.values():

            if cat.parent:
                parent_id = normalize(cat.parent)
                assert parent_id in self.categories.keys()
                cat.parent = self.categories[parent_id]

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

            if isinstance(tool.organization, str):
                org_id = normalize(tool.organization)
                assert org_id in self.organizations.keys()
                tool.organization = [self.organizations[org_id]]

            else:
                for i, org_id in enumerate(tool.organization):
                    org_id = normalize(org_id)
                    assert org_id in self.organizations.keys()
                    tool.organization[i] = self.organizations[org_id]

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

            for i, cat_id in enumerate(tool.category):
                cat_id = normalize(cat_id)
                assert cat_id in self.categories.keys()
                tool.category[i] = self.categories[cat_id]

            self.tools[tool_id] = tool

