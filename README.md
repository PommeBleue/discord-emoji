# Discord Emoji processing
## Requirements
`discordemoji` requires a python version greater than `3.6`, but no additional requirements in order to be run.
## Basic Usage
You can directly install the package using the `pip` module:
```shell
$ python3 -m pip install discordemoji
```
Or clone this repository and manually setup the package.

You can import the emojis dictionary by typing:
```python
from discordemoji import emojis
```
Allowing you to use it how you want to, or directly use the functions that the package provides:
```python
>>> from discordemoji import findall
>>> findall("Hi, my name is PommeBleue 🔵, but this heart is not blue : 💛")
['🔵', '💛']
```