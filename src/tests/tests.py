# -*- coding: utf-8 -*-
import demojiprocess

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


def test_function(f):
	def wrapper(*args, **kwargs):
		print("[INFO]", f"running tests for the {f.__name__[5:]} function.")
		f(*args, **kwargs)
		print("Tests passed.")

	return wrapper


@test_function
def test_is_valid_unicode():
	for emoji in test_emojis:
		assert demojiprocess.is_valid_unicode(emoji)
	assert not all((demojiprocess.is_valid_unicode(emoji) for emoji in test_unicode))
	assert not demojiprocess.is_valid_unicode("℔")
	assert not demojiprocess.is_valid_unicode("©")
	assert not demojiprocess.is_valid_unicode("☀︎")
	assert not demojiprocess.is_valid_unicode("♤")
	assert not demojiprocess.is_valid_unicode("♧")
	assert not demojiprocess.is_valid_unicode("♡")
	assert not demojiprocess.is_valid_unicode("♢")


@test_function
def test_names_of_unicode():
	assert demojiprocess.names_of_unicode("🤱🏻") == [':breast_feeding_tone1:', ':breast_feeding_light_skin_tone:', ':breast_feeding::skin-tone-1:']
	assert demojiprocess.names_of_unicode("🤙🏻") == [':call_me_tone1:', ':call_me_hand_tone1:', ':call_me::skin-tone-1:', ':call_me_hand::skin-tone-1:']
	assert demojiprocess.names_of_unicode("👫") == [':couple:', ':woman_and_man_holding_hands_tone1:', ':woman_and_man_holding_hands_light_skin_tone:', ':woman_and_man_holding_hands_tone1_tone2:', ':woman_and_man_holding_hands_light_skin_tone_medium_light_skin_tone:', ':woman_and_man_holding_hands_tone1_tone3:', ':woman_and_man_holding_hands_light_skin_tone_medium_skin_tone:', ':woman_and_man_holding_hands_tone1_tone4:', ':woman_and_man_holding_hands_light_skin_tone_medium_dark_skin_tone:', ':woman_and_man_holding_hands_tone1_tone5:', ':woman_and_man_holding_hands_light_skin_tone_dark_skin_tone:', ':woman_and_man_holding_hands_tone2:', ':woman_and_man_holding_hands_medium_light_skin_tone:', ':woman_and_man_holding_hands_tone2_tone1:', ':woman_and_man_holding_hands_medium_light_skin_tone_light_skin_tone:', ':woman_and_man_holding_hands_tone2_tone3:', ':woman_and_man_holding_hands_medium_light_skin_tone_medium_skin_tone:', ':woman_and_man_holding_hands_tone2_tone4:', ':woman_and_man_holding_hands_medium_light_skin_tone_medium_dark_skin_tone:', ':woman_and_man_holding_hands_tone2_tone5:', ':woman_and_man_holding_hands_medium_light_skin_tone_dark_skin_tone:', ':woman_and_man_holding_hands_tone3:', ':woman_and_man_holding_hands_medium_skin_tone:', ':woman_and_man_holding_hands_tone3_tone1:', ':woman_and_man_holding_hands_medium_skin_tone_light_skin_tone:', ':woman_and_man_holding_hands_tone3_tone2:', ':woman_and_man_holding_hands_medium_skin_tone_medium_light_skin_tone:', ':woman_and_man_holding_hands_tone3_tone4:', ':woman_and_man_holding_hands_medium_skin_tone_medium_dark_skin_tone:', ':woman_and_man_holding_hands_tone3_tone5:', ':woman_and_man_holding_hands_medium_skin_tone_dark_skin_tone:', ':woman_and_man_holding_hands_tone4:', ':woman_and_man_holding_hands_medium_dark_skin_tone:', ':woman_and_man_holding_hands_tone4_tone1:', ':woman_and_man_holding_hands_medium_dark_skin_tone_light_skin_tone:', ':woman_and_man_holding_hands_tone4_tone2:', ':woman_and_man_holding_hands_medium_dark_skin_tone_medium_light_skin_tone:', ':woman_and_man_holding_hands_tone4_tone3:', ':woman_and_man_holding_hands_medium_dark_skin_tone_medium_skin_tone:', ':woman_and_man_holding_hands_tone4_tone5:', ':woman_and_man_holding_hands_medium_dark_skin_tone_dark_skin_tone:', ':woman_and_man_holding_hands_tone5:', ':woman_and_man_holding_hands_dark_skin_tone:', ':woman_and_man_holding_hands_tone5_tone1:', ':woman_and_man_holding_hands_dark_skin_tone_light_skin_tone:', ':woman_and_man_holding_hands_tone5_tone2:', ':woman_and_man_holding_hands_dark_skin_tone_medium_light_skin_tone:', ':woman_and_man_holding_hands_tone5_tone3:', ':woman_and_man_holding_hands_dark_skin_tone_medium_skin_tone:', ':woman_and_man_holding_hands_tone5_tone4:', ':woman_and_man_holding_hands_dark_skin_tone_medium_dark_skin_tone:']
	assert demojiprocess.names_of_unicode("🗾") == [':japan:']
	assert demojiprocess.names_of_unicode("🗾", with_columns=False) == ['japan']
	assert demojiprocess.names_of_unicode("🧑🏾", with_columns=False) == ['adult_tone4', 'adult_medium_dark_skin_tone', 'adult:skin-tone-4']


@test_function
def test_unicode_of_name():
	assert demojiprocess.unicode_of_name("yellow_heart") == "💛"
	assert demojiprocess.unicode_of_name(":yellow_heart:") == "💛"
	assert demojiprocess.unicode_of_name("woman_health_worker_tone2") == "👩🏼‍⚕️"
	assert demojiprocess.unicode_of_name("adult:skin-tone-4") == "🧑🏾"


def test_code_point_of_name():
	assert demojiprocess.code_point_of_name("yellow_heart") == "1f49b"
	assert demojiprocess.code_point_of_name(":yellow_heart:") == "1f49b"
	assert demojiprocess.code_point_of_name("woman_health_worker_tone2") == "1f469-1f3fc-200d-2695-fe0f"
	assert demojiprocess.code_point_of_name("adult:skin-tone-4") == "1f9d1-1f3fe"


@test_function
def test_code_point_of_unicode():
	assert demojiprocess.code_point_of_unicode("🥐") == "1f950"
	assert demojiprocess.code_point_of_unicode("🧏🏻‍♂️") == "1f9cf-1f3fb-200d-2642-fe0f"
	assert demojiprocess.code_point_of_unicode("💵") == "1f4b5"
	assert demojiprocess.code_point_of_unicode("🏧") == "1f3e7"
	assert demojiprocess.code_point_of_unicode("🧑🏿‍🚀") == "1f9d1-1f3ff-200d-1f680"


@test_function
def test_findall():
	assert demojiprocess.findall(test_string) == test_emojis


@test_function
def test_replace():
	assert demojiprocess.replace("".join(test_emojis)) == ""


if __name__ == "__main__":
	test_is_valid_unicode()
	test_names_of_unicode()
	test_unicode_of_name()
	test_code_point_of_name()
	test_code_point_of_unicode()
	test_findall()
	test_replace()
