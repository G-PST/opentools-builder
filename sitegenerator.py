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

        self.templates = {
            "home": t_env.get_template("index.html"),
            "tool": t_env.get_template("tool.html"),
            "org": t_env.get_template("organization.html"),
        }


    def generate(self, baseurl: str, outpath: str):

        self.outpath = Path(outpath)
        self.baseurl = baseurl

        self.create_sitedir()

        self.generate_home()
        self.generate_tools()
        self.generate_orgs()

        self.generate_manifest()

    def get_toolpath(self, tool_id):
        return PurePosixPath("tools") / tool_id

    def get_toolurl(self, tool_id):
        relpath = self.get_toolpath(tool_id).as_posix()
        return urljoin(self.baseurl, relpath)

    def get_orgpath(self, org_id):
        return PurePosixPath("organizations") / org_id

    def get_orgurl(self, org_id):
        relpath = self.get_orgpath(org_id).as_posix()
        return urljoin(self.baseurl, relpath)

    def get_categorypath(self, cat_id):
        return PurePosixPath("categories") / cat_id

    def get_categoryurl(self, cat_id):
        relpath = self.get_categorypath(cat_id).as_posix()
        return urljoin(self.baseurl, relpath)

    def create_sitedir(self):
        shutil.rmtree(self.outpath, ignore_errors=True)
        shutil.copytree(self.static_path, self.outpath)

    def generate_home(self):

        template = self.templates["home"]
        filepath = self.outpath / "index.html"
        writefile(filepath, template.render(site=self))

    def generate_tools(self):

        template = self.templates["tool"]

        for tool_id, tool in self.data.tools.items():

            dir = self.outpath / self.get_toolpath(tool_id)
            filepath = dir / "index.html"

            os.makedirs(dir)
            writefile(filepath, template.render(site=self, tool=tool))

    def generate_orgs(self):

        template = self.templates["org"]

        for org_id, org in self.data.organizations.items():

            dir = self.outpath / self.get_orgpath(org_id)
            filepath = dir / "index.html"

            os.makedirs(dir)
            writefile(filepath, template.render(site=self, org=org))

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

