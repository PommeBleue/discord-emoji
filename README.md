# Discord Emoji processing
## Requirements
`discordemoji` requires a python version greater than `3.7`, but no additional requirements in order to be run.
## How it works
The script fetches emoji data from [here](https://emzi0767.mzgit.io/discord-emoji/discordEmojiMap-canary.min.json).
The first time you use it, it will store this data in a cache folder of your choosing, allowing you to load it for future uses.
By default the cache directory is `$HOME/.cache/discordEmojisMap/`
## Basic Usage
You can directly install the package using the `pip` module:
```shell
$ python3 -m pip install discordemoji
```
Or clone this repository and manually setup the package.

You can import the EmojiHandler class directly
```python
from discordemoji import EmojiHandler
```
Allowing you to set up your EmojiHandler instance by passing in the directory in which you want to cache the emoji data json file.
```python
from discordemoji import EmojiHandler

emoji = EmojiHandler()
print(emoji.findall("Hi, my name is PommeBleue 🔵, but this heart is not blue : 💛"))
# ['🔵', '💛']
```