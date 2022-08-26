# Standard modules
from enum import Enum


class Pattern(Enum):
    URL = 1


class Mode(Enum):
    QUERY = "queries"
    MUTATION = "mutations"
