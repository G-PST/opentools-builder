import io
import os
from pathlib import Path, PurePosixPath
import shutil
from urllib.parse import urljoin

import jinja2

from portaldata import PortalData

def writefile(filepath: Path, text: str):

    with io.open(filepath, 'w') as f:
        f.write(text)

class PortalSite():

    def __init__(self, data: PortalData):

        self.data = data

        t_env = jinja2.Environment(
                    loader=jinja2.FileSystemLoader("templates"),
                    autoescape=jinja2.select_autoescape())

        self.templates = {
            "home": t_env.get_template("index.html"),
            "tool": t_env.get_template("tool.html"),
            "org": t_env.get_template("organization.html"),
        }


    def generate(self, baseurl: str, outpath: str):

        self.outpath = Path(outpath)
        shutil.rmtree(self.outpath, ignore_errors=True)
        os.makedirs(self.outpath)

        self.baseurl = baseurl

        self.generate_home()
        self.generate_tools()
        self.generate_orgs()

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
