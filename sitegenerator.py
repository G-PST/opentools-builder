import io
import os
from pathlib import Path, PurePosixPath
import shutil
from urllib.parse import urljoin

import jinja2

from portaldata import PortalData
import util

def writefile(filepath: Path, text: str):

    with io.open(filepath, 'w') as f:
        f.write(text)

def make_manifest(vals: dict):

    return [
        { "id": id, "name": val.name }
        for id, val in vals.items()
    ]

class PortalSite():

    def __init__(self, data: PortalData, template_path: str, static_path: str):

        self.data = data
        self.template_path = template_path
        self.static_path = static_path

        t_env = jinja2.Environment(
                    loader=jinja2.FileSystemLoader(self.template_path),
                    autoescape=jinja2.select_autoescape())

        self.entity_names = {
            "tools": "tool",
            "organizations": "org",
            "categories": "category",
            "programming-languages": "proglang",
            "licenses": "license",
        }

        self.templates = {
            "home": t_env.get_template("index.html"),
            "tools": t_env.get_template("tool.html"),
            "organizations": t_env.get_template("organization.html"),
            "categories": t_env.get_template("category.html"),
            "programming-languages": t_env.get_template("programminglanguage.html"),
            "licenses": t_env.get_template("license.html"),
        }

        self.index_templates = {
            "tools": t_env.get_template("tool_index.html"),
            "organizations": t_env.get_template("org_index.html"),
        }


    def generate(self, baseurl: str, outpath: str):

        self.outpath = Path(outpath)
        self.baseurl = baseurl
        self.tools_url = urljoin(baseurl, "tools")
        self.orgs_url = urljoin(baseurl, "organizations")

        self.create_sitedir()

        self.generate_home()
        self.generate_manifest()

        self.generate_pages("tools", self.data.tools)
        self.generate_pages("organizations", self.data.organizations)
        self.generate_pages("categories", self.data.categories)
        self.generate_pages("programming-languages", self.data.languages)
        self.generate_pages("licenses", self.data.licenses)

    def get_url(self, entity):
        return urljoin(self.baseurl, entity.path.as_posix())

    def create_sitedir(self):
        shutil.rmtree(self.outpath, ignore_errors=True)
        shutil.copytree(self.static_path, self.outpath)

    def generate_home(self):

        template = self.templates["home"]
        filepath = self.outpath / "index.html"
        writefile(filepath, template.render(site=self))

    def generate_pages(self, entity_type: str, entities):

        template = self.templates[entity_type]

        for entity in entities.values():

            dir = self.outpath / entity.path
            os.makedirs(dir)
            template_args = {
                "site": self,
                self.entity_names[entity_type]: entity
            }
            writefile(dir / "index.html", template.render(**template_args))

        if entity_type in self.index_templates:

            template = self.index_templates[entity_type]
            filepath = self.outpath / entity_type / "index.html"
            writefile(filepath, template.render(site=self))

    def generate_manifest(self):

        manifest = {
            "licenses": make_manifest(self.data.licenses),
            "organizations": make_manifest(self.data.organizations),
            "categories": make_manifest(self.data.categories),
            "languages": make_manifest(self.data.languages),
            "software": make_manifest(self.data.tools),
        }

        filepath = self.outpath / "manifest.json"

        util.write_file(manifest, filepath)

