#!/usr/bin/env python3.6

# Import modules

import re
import unidecode


def cleanse_names(name):

    name = name.replace("+ ", "plus_")
    name = name.replace(" -", "_")
    name = name.replace("  ", "_")
    name = name.replace(" ", "_")
    name = name.replace("/", "_")
    name = name.replace(".", "_")
    name = unidecode.unidecode(name)
    valid_chars = re.compile(r"[^A-Za-z0-9!@#$%^&()-_{}]")
    name = valid_chars.sub("", name)

    return name
