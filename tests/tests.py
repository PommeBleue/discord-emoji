# -*- coding: utf-8 -*-
import discordemoji

from random import randint

test_emojis = [
	"❤️",
	"🧡",
	"💛",
	"💚",
	"💙",
	"💜",
	"😭",
	"👀",
	"🥄",
	"🖊️"
]

test_unicode = [
	"💛",
	"😭",
	"👀",
	"🥄",
	"🖊",
	"我喜欢Discord。",
	"В последнее время было жарко.",
	"💻",
	"Je suis la plus belle patate de cette assiette.",
	"☼"
]

test_string = ("".join([chr(randint(0, 1000)) for i in range(randint(0, 1000))])).join(test_emojis)

emojis = discordemoji.EmojiHandler()


def test_function(f):
	def wrapper(*args, **kwargs):
		print("[INFO]", f"running tests for the {f.__name__[5:]} function.")
		f(*args, **kwargs)
		print("[INFO]", f"Tests for {f.__name__[5:]} passed ✅.")

	return wrapper


@test_function
def test_is_valid_unicode():
	for emoji in test_emojis:
		assert emojis.is_valid_unicode(emoji)
	assert not all((emojis.is_valid_unicode(emoji) for emoji in test_unicode))
	assert not emojis.is_valid_unicode("℔")
	assert not emojis.is_valid_unicode("☀︎")
	assert not emojis.is_valid_unicode("♤")
	assert not emojis.is_valid_unicode("♧")
	assert not emojis.is_valid_unicode("♡")
	assert not emojis.is_valid_unicode("♢")


@test_function
def test_names_of_unicode():
	assert emojis.names_of_unicode("🏂🏻") == [":snowboarder_tone1:", ":snowboarder_light_skin_tone:", ":snowboarder::skin-tone-1:"]
	assert emojis.names_of_unicode("👎🏾") == [":thumbsdown_tone4:", ":_1_tone4:", ":thumbdown_tone4:", ":thumbsdown::skin-tone-4:", ":-1::skin-tone-4:", ":thumbdown::skin-tone-4:", ":thumbs_down::skin-tone-4:"]
	assert emojis.names_of_unicode("🎌") == [":crossed_flags:"]
	assert emojis.names_of_unicode("👨🏿‍🔬", with_columns=False) == ["man_scientist_tone5", "man_scientist_dark_skin_tone", "man_scientist:skin-tone-5"]
	assert emojis.names_of_unicode("🎌", with_columns=False) == ["crossed_flags"]
	assert emojis.names_of_unicode("👩🏾‍🌾", with_columns=False) == ["woman_farmer_tone4", "woman_farmer_medium_dark_skin_tone", "woman_farmer:skin-tone-4"]


@test_function
def test_unicode_of_name():
	assert emojis.unicode_of_name("yellow_heart") == "💛"
	assert emojis.unicode_of_name(":yellow_heart:") == "💛"
	assert emojis.unicode_of_name("woman_health_worker_tone2") == "👩🏼‍⚕️"
	assert emojis.unicode_of_name("adult:skin-tone-4") == "🧑🏾"


def test_code_point_of_name():
	assert emojis.code_point_of_name("yellow_heart") == "1f49b"
	assert emojis.code_point_of_name(":yellow_heart:") == "1f49b"
	assert emojis.code_point_of_name("woman_health_worker_tone2") == "1f469-1f3fc-200d-2695-fe0f"
	assert emojis.code_point_of_name("adult:skin-tone-4") == "1f9d1-1f3fe"


@test_function
def test_code_point_of_unicode():
	assert emojis.code_point_of_unicode("🥐") == "1f950"
	assert emojis.code_point_of_unicode("🧏🏻‍♂️") == "1f9cf-1f3fb-200d-2642-fe0f"
	assert emojis.code_point_of_unicode("💵") == "1f4b5"
	assert emojis.code_point_of_unicode("🏧") == "1f3e7"
	assert emojis.code_point_of_unicode("🧑🏿‍🚀") == "1f9d1-1f3ff-200d-1f680"


@test_function
def test_findall():
	assert emojis.findall(test_string) == test_emojis


@test_function
def test_replace():
	assert emojis.replace("".join(test_emojis)) == ""


if __name__ == "__main__":
	test_is_valid_unicode()
	test_names_of_unicode()
	test_unicode_of_name()
	test_code_point_of_name()
	test_code_point_of_unicode()
	test_findall()
	test_replace()
