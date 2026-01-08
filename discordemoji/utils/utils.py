"""Data is imported from  https://static.emzi0767.com/misc/discordEmojiMap.min.json
"""

import re
import os

def cleaned(name):
    match = re.match(r"^:(.+):$", name)
    if match:
        return ":".join(match[1].split("::"))
    return name


def pattern_from(unicode_entities):
    return re.compile(r"|".join((re.escape(code) for code in sorted(unicode_entities, key=len, reverse=True))))