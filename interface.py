""" This module contains all the interfaces for data models used."""

# standard imports
from typing import Optional, List

# third-party imports
from pydantic import BaseModel


class ProgrammingLanguage(BaseModel):
    """Interface for programming language."""

    name: str
    url: str
    license: List[str]
    description: Optional[str] = None


class Licenses(BaseModel):
    """Interface for opensource licenses."""

    name: str
    spdx_id: str


class Organization(BaseModel):
    """Interface for organization."""

    name: str
    description: Optional[str] = None
    url: Optional[str] = None


class ToolCategory(BaseModel):
    """Interface for tree of software tool categorizations."""

    name: str
    parent: Optional[str]
    description: Optional[str]


class SoftwareTool(BaseModel):
    """ Interface for software tool. """

    name: str 
    category: List[str]
    language: List[str]
    organization: List[str]
    license: List[str]
    description: Optional[str] = None
    url_website: Optional[str] = None
    url_sourcecode: Optional[str] = None
    url_docs: Optional[str] = None
