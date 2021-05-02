# -*- coding: utf-8 -*-

"""Simple functions to detect, replace, remove, or convert to code point a string containing unicode emojis or emojis that are supported by Discord.

https://static.emzi0767.com/misc/discordEmojiMap.min.json
"""

from .resources import emojis, sijome
import re

_PATTERN = None


def _cleaned(name):
    match = re.match(r"^:(.+):$", name)
    if match:
        return ":".join(match[1].split("::"))
    return name


def _pattern_from(unicode_entities):
    return re.compile(r"|".join((re.escape(code) for code in sorted(unicode_entities, key=len, reverse=True))))


def _set_pattern():
    global _PATTERN
    if _PATTERN is None:
        _PATTERN = _pattern_from(emojis)


def is_valid_unicode(unicode_entity):
    """Checks if a given unicode entity is valid, meaning that it's contained in the dictionary.

    :param unicode_entity:
    :type unicode_entity: str
    :returns: True if the given unicode entity is valid, False if not.
    :rtype: bool
    """
    return unicode_entity in emojis.keys()


def names_of_unicode(unicode_entity, with_columns=True):
    """Returns all the names used by Discord to represent the given unicode entity.

    :param unicode_entity:
    :type unicode_entity: str
    :param with_columns: Whether the function should return the list of names with columns, or without columns.
    :type with_columns: bool
    :returns: The list of all the names.
    :rtype: list
    """
    if is_valid_unicode(unicode_entity):
        names = emojis[unicode_entity]
        if with_columns:
            return names
        return [_cleaned(name) for name in names]
    raise ValueError("The given argument unicode_to_replace isn't valid.")


def unicode_of_name(name):
    """Returns the unicode that the given name represents.

    :param name: The name corresponding to the wanted unicode entity.
    :type name: str
    :returns: The unicode entity.
    :rtype: str
    """
    if name not in sijome.keys():
        name = ":{name}:".format(name="::".join(name.split(":")))
        if name in sijome.keys():
            return sijome[name]
        raise ValueError("The given name isn't valid.")
    return sijome[name]


def code_point_of_unicode(unicode_entity, sep="-"):
    """Converts a given unicode entity to code point.

    :param unicode_entity: The unicode entity to convert.
    :type unicode_entity: str
    :param sep: The separator. The result will be the list of all the converted characters joined with this separator.
    :type sep: str
    :returns: The converted string.
    :rtype: str
    """
    # Source: https://github.com/twitter/twemoji/blob/master/scripts/build.js#L571
    result, current, p = [], 0, 0
    for i in range(len(unicode_entity)):
        current = ord(unicode_entity[i])
        if p:
            result.append("{a:02x}".format(a=0x10000 + ((p - 0xD800) << 10) + (current - 0xDC00)))
        elif 0xD800 <= current <= 0xDBFF:
            p = current
        else:
            result.append("{a:02x}".format(a=current))
    return sep.join(result)


def code_point_of_name(name, sep="-"):
    """Converts the unicode entity that corresponds to the given name to code point.

    :param name: A name that matches the wanted unicode_entity.
    :type name: str
    :param sep: The separator. The result will be the list of all the converted characters joined with this separator.
    :type sep: str
    :returns: The converted string.
    :rtype: str
    """
    unicode_entity = unicode_of_name(name)
    return code_point_of_unicode(unicode_entity, sep)


def findall(string):
    """Find all valid unicode entities in the given string, and returns them as a list.

    :param string:
    :type string: str
    :returns: List of all valid unicode entities.
    :rtype: list
    """
    _set_pattern()
    return _PATTERN.findall(string)


def replace(string, rep=""):
    """Replaces all valid unicode entities in the given string by the content of rep (empty by default).

    :param string: The string to modify.
    :type string: str
    :param rep: The string that will replace all the valid unicode entities.
    :type string: str
    :returns: The final string
    :rtype: str
    """
    _set_pattern()
    return _PATTERN.sub(rep, string)
