from interface import (
    ProgrammingLanguage,
    Licenses,
    Organization,
    ToolCategory,
    SoftwareTool,
)

from pathlib import Path, PurePosixPath
from pydantic import ValidationError
from util import read_file, write_file

def normalize(x: str):
    return x.lower().replace(" ", "")

class PortalData():

    def __init__(self, datapath: str):

        datapath = Path(datapath)

        self.errors = []

        self.load_licenses(datapath)
        self.load_organizations(datapath)
        self.load_categories(datapath)
        self.load_languages(datapath)
        self.load_tools(datapath)

    def load_licenses(self, datapath: Path):

        self.licenses = {}

        for file in (datapath / "licenses").iterdir():

            try:
                licen = Licenses.model_validate(read_file(file))

            except ValidationError as err:
                self.errors.append(("licenses", file.name, str(err)))
                continue

            licen.id = file.name.replace(file.suffix, "")
            licen.path = PurePosixPath("licenses") / licen.id
            licen.tools = []

            self.licenses[licen.id] = licen

    def load_languages(self, datapath: Path):

        self.languages = {}

        for file in (datapath / "languages").iterdir():

            try:
                lang = ProgrammingLanguage.model_validate(read_file(file))

            except ValidationError as err:
                self.errors.append(("languages", file.name, str(err)))
                continue

            lang.id = file.name.replace(file.suffix, "")
            lang.path = PurePosixPath("programming-languages") / lang.id
            lang.tools = []

            for i, licen_id in enumerate(lang.licenses):

                licen_id = normalize(licen_id)

                if licen_id not in self.licenses.keys():
                    self.errors.append(("languages", file.name,
                         f"'{licen_id}' is not a valid licence id"))
                    continue

                lang.licenses[i] = self.licenses[licen_id]

            self.languages[lang.id] = lang

    def load_organizations(self, datapath: Path):

        self.organizations = {}

        for file in (datapath / "organizations").iterdir():

            try:
                org = Organization.model_validate(read_file(file))

            except ValidationError as err:
                self.errors.append(("organizations", file.name, str(err)))
                continue

            org.id = file.name.replace(file.suffix, "")
            org.path = PurePosixPath("organizations") / org.id
            org.tools = []

            self.organizations[org.id] = org

    def load_categories(self, datapath: Path):

        self.categories = {}

        for file in (datapath / "categories").iterdir():

            try:
                cat = ToolCategory.model_validate(read_file(file))

            except ValidationError as err:
                self.errors.append(("categories", file.name, str(err)))
                continue

            cat.id = file.name.replace(file.suffix, "")
            cat.path = PurePosixPath("categories") / cat.id
            cat.children = []
            cat.tools = []

            self.categories[cat.id] = cat

        for cat in self.categories.values():

            if cat.parent:

                parent_id = normalize(cat.parent)

                if parent_id not in self.categories.keys():
                    self.errors.append(("categories", cat.id,
                         f"'{parent_id}' is not a valid parent category id"))
                    continue

                cat.parent = self.categories[parent_id]
                cat.parent.children.append(cat)

    def load_tools(self, datapath: Path):

        self.tools = {}

        for file in (datapath /"software").iterdir():

            try:
                tool = SoftwareTool.model_validate(read_file(file))

            except ValidationError as err:
                self.errors.append(("software", file.name, str(err)))
                continue

            tool.id = file.name.replace(file.suffix, "")
            tool.path = PurePosixPath("tools") / tool.id

            for i, lang_id in enumerate(tool.languages):

                lang_id = normalize(lang_id)

                if lang_id not in self.languages.keys():
                    self.errors.append(("software", file.name,
                         f"'{lang_id}' is not a valid programming language id"))
                    continue

                lang = self.languages[lang_id]
                tool.languages[i] = lang
                lang.tools.append(tool)

            for i, org_id in enumerate(tool.organizations):

                org_id = normalize(org_id)

                if org_id not in self.organizations.keys():
                    self.errors.append(("software", file.name,
                         f"'{org_id}' is not a valid organization id"))
                    continue

                org = self.organizations[org_id]
                tool.organizations[i] = org
                org.tools.append(tool)

            for i, licen_id in enumerate(tool.licenses):

                licen_id = normalize(licen_id)

                if licen_id not in self.licenses.keys():
                    self.errors.append(("software", file.name,
                         f"'{licen_id}' is not a valid license id"))
                    continue

                licen = self.licenses[licen_id]
                tool.licenses[i] = licen
                licen.tools.append(tool)

            for i, cat_id in enumerate(tool.categories):

                cat_id = normalize(cat_id)

                if cat_id not in self.categories.keys():
                    self.errors.append(("software", file.name,
                         f"'{cat_id}' is not a valid category id"))
                    continue

                cat = self.categories[cat_id]
                tool.categories[i] = cat
                cat.tools.append(tool)

            self.tools[tool.id] = tool

    def has_errors(self):
        return len(self.errors) > 0

    def write_errormessage(self, errorpath: Path):
        with open(errorpath, 'w') as f:

            f.write("Thank you for your submission! " +
            "Unfortunately, we could not successfully parse the dataset " +
            "after applying your changes. Here are the errors we encountered:" +
            "\n\n```\n")

            for error in self.errors:
                f.write(str(error) + "\n")

            f.write("```\n\n" +
            "If you can, try fixing these and update your submission.\n")
