# -*- coding: utf-8 -*-

"""Simple functions to detect, replace, remove, or convert to code point a string containing unicode emojis or emojis that are supported by Discord.

https://static.emzi0767.com/misc/discordEmojiMap.min.json
"""

import re
import json
import urllib.request
import logging

from os import PathLike
from typing import Iterator, Any
from .utils import pattern_from, cleaned
from urllib.error import URLError
from datetime import datetime
from pathlib import Path


SOURCE_URL = 'https://static.emzi0767.com/misc/discordEmojiMap.min.json'
DEFINITIONS_KEY = 'emojiDefinitions'
VERSION_TIMESTAMP_KEY = 'versionTimestamp'


logging.basicConfig(
    format='%(asctime)s;%(levelname)s;%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class EmojiHandler:
    emojis : list[dict[str, Any]] = []
    _version : float | None = None
    _pattern : re.Pattern | None = None
    _unicode_map : dict[str, dict[str, Any]] = {}
    _name_map : dict[str, dict[str, Any]] = {}


    def __init__(self, cache_dir: str | PathLike[str] | None = None) -> None:
        """Init with option cache dir."""

        self.cache_dir = Path(__file__) / cache_dir if cache_dir else Path.home() / 'discordEmojisMap'
        self.cache_file = self.cache_dir / 'emojis.json'
        self._get()
        self._build_lookups()
        self._set_pattern()


    def _get(self) -> None:
        """Load emoji data from cache or request from SOURCE_URL."""

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


    def _set_pattern(self) -> None:
        """Compile pattern for emoji detection."""

        self._pattern = pattern_from(list(self.surrogates()))


    def _build_lookups(self) -> None:
        """Emojis lookup helpers."""

        self._unicode_map = {
            emoji.get('surrogates'): emoji
            for emoji in self.emojis
        }

        self._name_map = {}
        for emoji in self.emojis:
            for name in emoji.get('names', []):
                self._name_map[name] = emoji


    def refresh(self) -> None:
        """Fetch latest emoji data and update the cache file accordingly"""
        
        try:
            logger.info('Attempting to reload emoji data.')
            self.cache_dir.mkdir(parents=True, exist_ok=True)

            with urllib.request.urlopen(SOURCE_URL) as response:
                data = json.load(response)

            version_timestamp = datetime.fromisoformat(data.get(VERSION_TIMESTAMP_KEY)).timestamp()

            if self._version is None or self._version < version_timestamp:
                emoji_data = data.get(DEFINITIONS_KEY)

                if emoji_data:
                    with open(self.cache_file, 'w') as f:
                        json.dump(data, f)

                    self.emojis = emoji_data
                    self._version = version_timestamp
                    self._build_lookups()
                    self._set_pattern()
                    logger.info(f'Updated to version {version_timestamp}. Fetched {len(self.emojis)} emojis.')
                else:
                    logger.error('No emoji data found in response.')
            else:
                logger.info('Emoji data already up to date.')

        except URLError:
            logger.error('Something went wrong while attempting to request the json file.')


    def surrogates(self) -> Iterator[str]:
        for emoji in self.emojis:
            if surrogate := emoji.get('surrogates'):
                yield surrogate


    def emoji_of_unicode(self, unicode_entity : str) -> dict:
        """

        :param unicode_entity:
        :return:
        """
        return self._unicode_map.get(unicode_entity)


    def emoji_of_name(self, name : str) -> dict:
        """

        :param name:
        :return:
        """
        return self._name_map.get(cleaned(name))


    def is_valid_unicode(self, unicode_entity : str) -> bool:
        """Checks if a given Unicode entity is valid, meaning that it's one of the emojis surrogates field.

        :param unicode_entity:
        :type unicode_entity: str
        :return: True iff the given Unicode entity is valid.
        :rtype: bool
        """
        return unicode_entity in self._unicode_map


    def names_of_unicode(self, unicode_entity : str, with_colons : bool = True) -> list[str,]:
        """Returns the names of the corresponding Unicode entity if it exists and None otherwise.

        :param unicode_entity:
        :param with_colons:
        :return:
        """
        emoji = self.emoji_of_unicode(unicode_entity)
        if emoji:
            key = 'namesWithColons' if with_colons else 'names'
            return emoji.get(key, [])
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


    def unicode_of_name(self, name: str) -> str:
        """

        :param name:
        :return:
        """
        emoji = self.emoji_of_name(name)
        if emoji is not None:
            return emoji.get('surrogates')
        raise ValueError('Name {name} is not valid emoji name.'.format(name=name))


    def code_point_of_name(self, name: str, sep: str = "-") -> str:
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


    def findall(self, text : str) -> list[str,]:
        """

        :param text:
        :return:
        """
        return self._pattern.findall(text)


    def replace(self, text : str, rep : str ="") -> str:
        """
        s
        :param text:
        :param rep:
        :return:
        """
        return self._pattern.sub(rep, text)
