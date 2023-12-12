from interface import (
    ProgrammingLanguage,
    Licenses,
    Organization,
    ToolCategory,
    SoftwareTool,
)

from pathlib import Path, PurePosixPath
from util import read_file, write_file


def normalize(x: str):
    return x.lower().replace(" ", "")

class PortalData():

    def __init__(self, datapath: str):

        datapath = Path(datapath)

        self.load_licenses(datapath)
        self.load_organizations(datapath)
        self.load_categories(datapath)
        self.load_languages(datapath)
        self.load_tools(datapath)

    def load_languages(self, datapath: Path):

        self.languages = {}

        for file in (datapath / "languages").iterdir():

            lang = ProgrammingLanguage.model_validate(read_file(file))

            lang.id = file.name.replace(file.suffix, "")
            lang.path = PurePosixPath("programming-languages") / lang.id
            lang.tools = []

            for i, licen_id in enumerate(lang.licenses):
                licen_id = normalize(licen_id)
                assert licen_id in self.licenses.keys()
                lang.licenses[i] = self.licenses[licen_id]

            self.languages[lang.id] = lang

    def load_licenses(self, datapath: Path):

        self.licenses = {}

        for file in (datapath / "licenses").iterdir():

            licen = Licenses.model_validate(read_file(file))

            licen.id = file.name.replace(file.suffix, "")
            licen.path = PurePosixPath("licenses") / licen.id
            licen.tools = []

            self.licenses[licen.id] = licen

    def load_organizations(self, datapath: Path):

        self.organizations = {}

        for file in (datapath / "organizations").iterdir():

            org = Organization.model_validate(read_file(file))

            org.id = file.name.replace(file.suffix, "")
            org.path = PurePosixPath("organizations") / org.id
            org.tools = []

            self.organizations[org.id] = org

    def load_categories(self, datapath: Path):

        self.categories = {}

        for file in (datapath / "categories").iterdir():

            cat = ToolCategory.model_validate(read_file(file))

            cat.id = file.name.replace(file.suffix, "")
            cat.path = PurePosixPath("categories") / cat.id
            cat.children = []
            cat.tools = []

            self.categories[cat.id] = cat

        for cat in self.categories.values():

            if cat.parent:
                parent_id = normalize(cat.parent)
                assert parent_id in self.categories.keys()
                cat.parent = self.categories[parent_id]
                cat.parent.children.append(cat)

    def load_tools(self, datapath: Path):

        self.tools = {}

        for file in (datapath /"software").iterdir():

            tool = SoftwareTool.model_validate(read_file(file))
            tool.id = file.name.replace(file.suffix, "")
            tool.path = PurePosixPath("tools") / tool.id

            for i, lang_id in enumerate(tool.languages):
                lang_id = normalize(lang_id)
                assert lang_id in self.languages.keys()
                lang = self.languages[lang_id]
                tool.languages[i] = lang
                lang.tools.append(tool)

            for i, org_id in enumerate(tool.organizations):
                org_id = normalize(org_id)
                assert org_id in self.organizations.keys()
                org = self.organizations[org_id]
                tool.organizations[i] = org
                org.tools.append(tool)

            for i, licen_id in enumerate(tool.licenses):
                licen_id = normalize(licen_id)
                assert licen_id in self.licenses.keys()
                licen = self.licenses[licen_id]
                tool.licenses[i] = licen
                licen.tools.append(tool)

            for i, cat_id in enumerate(tool.categories):
                cat_id = normalize(cat_id)
                assert cat_id in self.categories.keys()
                cat = self.categories[cat_id]
                tool.categories[i] = cat
                cat.tools.append(tool)

            self.tools[tool.id] = tool

