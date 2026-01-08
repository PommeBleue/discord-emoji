# -*- coding: utf-8 -*-

"""Simple functions to detect, replace, remove, or convert to code point a string containing unicode emojis or emojis that are supported by Discord.

https://static.emzi0767.com/misc/discordEmojiMap.min.json
"""

from .utils import pattern_from
from urllib.error import URLError
from datetime import datetime
from pathlib import Path

import json
import urllib.request

SOURCE_URL = 'https://static.emzi0767.com/misc/discordEmojiMap.min.json'
DEFINITIONS_KEY = 'emojiDefinitions'
VERSION_TIMESTAMP_KEY = 'versionTimestamp'


class EmojiHandler:
    emojis = []
    _version = None
    _pattern = None

    def __init__(self, cache_dir=None):
        self.cache_dir = Path(__file__) / cache_dir if cache_dir else Path.home() / 'discordEmojisMap'
        self.cache_file = self.cache_dir / 'emojis.json'
        self._get()
        self._set_pattern()


    def _get(self):
        if self.cache_file.exists():
            try:
                with self.cache_file.open() as f:
                    data = json.load(f)
                    emoji_data, version = data.get(DEFINITIONS_KEY), datetime.fromisoformat(data.get(VERSION_TIMESTAMP_KEY)).timestamp()

                    self.emojis = emoji_data
                    self._version = version

            except (json.JSONDecodeError, OSError):
                pass

        self.refresh()


    def _set_pattern(self):
        self._pattern = pattern_from(list(self.surrogates()))


    def refresh(self):
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

            with urllib.request.urlopen(SOURCE_URL) as response:
                data = json.load(response)

            version_timestamp = datetime.fromisoformat(data.get(VERSION_TIMESTAMP_KEY)).timestamp()

            if self._version is None or self._version < version_timestamp:
                emoji_data = data.get(DEFINITIONS_KEY)
                with open(self.cache_file, 'w') as f:
                    json.dump(data, f)

                self.emojis = emoji_data
                self._version = version_timestamp

        except URLError:
            pass


    def surrogates(self):
        for emoji in self.emojis:
            yield emoji.get('surrogates')


    def emoji_of_unicode(self, unicode_entity : str) -> dict:
        """

        :param unicode_entity:
        :return:
        """
        return next((emoji for emoji in self.emojis if emoji.get('surrogates') == unicode_entity), None)


    def emoji_of_name(self, name : str) -> dict:
        """

        :param name:
        :return:
        """
        return next((emoji for emoji in self.emojis if name in emoji.get('names') or name in emoji.get('namesWithColons')))


    def is_valid_unicode(self, unicode_entity : str) -> bool:
        """Checks if a given Unicode entity is valid, meaning that it's one of the emojis surrogates field.

        :param unicode_entity:
        :type unicode_entity: str
        :return: True iff the given Unicode entity is valid.
        :rtype: bool
        """
        emoji = self.emoji_of_unicode(unicode_entity)
        return emoji is not None


    def names_of_unicode(self, unicode_entity : str, with_columns : bool = True) -> list[str,] | None:
        """Returns the names of the corresponding Unicode entity if it exists and None otherwise.

        :param unicode_entity:
        :param with_columns:
        :return:
        """
        emoji = self.emoji_of_unicode(unicode_entity)
        if emoji:
            if with_columns:
                return emoji.get('namesWithColons')
            return emoji.get('names')
        raise ValueError('Not a valid unicode_entity.')


    @staticmethod
    def code_point_of_unicode(unicode_entity : str, sep : str = "-") -> str:
        """Converts a given Unicode entity to code point.

        :param unicode_entity: The Unicode entity to convert.
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


    def unicode_of_name(self, name):
        """

        :param name:
        :return:
        """
        emoji = self.emoji_of_name(name)
        if emoji is not None:
            return emoji.get('surrogates')
        raise ValueError('Name {name} is not valid emoji name.'.format(name=name))


    def code_point_of_name(self, name, sep="-"):
        """Converts the Unicode entity that corresponds to the given name to code point.

        :param name: A name that matches the wanted unicode_entity.
        :type name: str
        :param sep: The separator. The result will be the list of all the converted characters joined with this separator.
        :type sep: str
        :returns: The converted string.
        :rtype: str
        """
        unicode_entity = self.unicode_of_name(name)
        return self.code_point_of_unicode(unicode_entity, sep)


    def findall(self, text):
        """

        :param text:
        :return:
        """
        return self._pattern.findall(text)


    def replace(self, text, rep=""):
        """
        s
        :param text:
        :param rep:
        :return:
        """
        return self._pattern.sub(rep, text)
