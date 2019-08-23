#!/usr/bin/env python
from typing import NamedTuple


class OmenName(NamedTuple):
    chapter: str
    omen: str
    tradition: str = None
    siglum: str = None



