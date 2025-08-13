import pytest
import json
from build_sentences import (get_seven_letter_word, parse_json_from_file, choose_sentence_structure,
                              get_pronoun, get_article, get_word, fix_agreement, build_sentence, structures)

def test_get_seven_letter_word(mocker):
    # PASSES when input length is 'more than 7'
    mock_input_one = mocker.patch("builtins.input", return_value = "MORETHAN7")
    res_more_than_seven = get_seven_letter_word()
    assert res_more_than_seven == "MORETHAN7"
    mock_input_one.assert_called_once_with("Please enter a word with at least 7 letters: ")

    # PASSES when input length is 'exactly 7'
    mock_input_two = mocker.patch("builtins.input", return_value = "ISSEVEN")
    res_is_seven = get_seven_letter_word()
    assert res_is_seven == "ISSEVEN"
    mock_input_two.assert_called_once_with("Please enter a word with at least 7 letters: ")

    # FAILS when there is no input 
    mock_input_three = mocker.patch("builtins.input", return_value = "")
    with pytest.raises(ValueError):
        get_seven_letter_word()
    mock_input_three.assert_called_once_with("Please enter a word with at least 7 letters: ")

def test_parse_json_from_file(mocker):
    # PASSES when the 'path' for the file is correct and the content is in JSON
    mock_open_one = mocker.patch("builtins.open", mocker.mock_open(read_data = '{"python" : "test"}'))
    res_pass = parse_json_from_file("test.txt")
    assert res_pass == {'python' : 'test'}
    mock_open_one.assert_called_once_with("test.txt", 'r')

    # FAILS when the 'path' for the file is incorrect
    mock_open_two = mocker.patch("builtins.open", side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        parse_json_from_file("fail.txt")
    mock_open_two.assert_called_once_with("fail.txt", 'r')

    # FAILS when the content is not in JSON
    mock_open_two = mocker.patch("builtins.open", mocker.mock_open(read_data = '{python : test}'))
    with pytest.raises(ValueError):
        parse_json_from_file("test.txt")
    mock_open_two.assert_called_once_with("test.txt",'r')

def test_choose_sentence_structure():
    choice = choose_sentence_structure()
    assert choice in structures

def test_get_pronoun(mocker):
    mock_choice = mocker.patch("random.choice", return_value = "we")
    assert get_pronoun() == "we"
    mock_choice.assert_called_once()

def test_get_article(mocker):
    mock_choice = mocker.patch("random.choice", return_value = "a")
    assert get_article() == "a"
    mock_choice.assert_called_once()

def test_get_word():
    # PASSES when the parameters 'letter' is type char, and 'speech_part' is type string
    assert get_word('A', "Faraday") == 'F'

    # FAILS when the parameter 'letter' is not type char
    with pytest.raises(TypeError):
        get_word(1, "Faraday")

    # FAILS when the parameter 'speech_part' is not type string
    with pytest.raises(TypeError):
        get_word('A', 12345)

    # FAILS when the parameter 'speech-part' is shorter than converted 'letter' index value
    with pytest.raises(IndexError):
        get_word('z', 'Faraday')


def test_fix_agreement():
    # PASSES condition 1
    sentence_one = ['he', 'quickly', 'walk']
    fix_agreement(sentence_one)
    assert sentence_one[0] == 'he'
    assert sentence_one[2] == 'walks'

    # PASSES condition 2
    sentence_two = ['a', 'beautiful', 'ocean']
    fix_agreement(sentence_two)
    assert sentence_two[0] == 'an'
    assert sentence_two[2] == 'ocean'

    # PASSES condition 3
    sentence_three = ['the', 'big', 'dog', 'happily', 'jump']
    fix_agreement(sentence_three)
    assert sentence_three[0] == 'the'
    assert sentence_three[4] == 'jumps'

def test_build_sentence(mocker):
    word = "AAAAAAA"
    structure = ["PRO","ADV","VERB","PREP","ART","ADJ","NOUN"]
    data = {
        "nouns": [
            "apples",
            "book",
            "cat"
        ],
        "verbs": [
            "run",
            "listen",
            "sing"
        ],
        "prepositions": [
            "about",
            "before",
            "from"
        ],
        "adjectives": [
            "happy",
            "big",
            "beautiful"
        ],
        "adverbs": [
            "often",
            "simply",
            "then"
        ]
    }

    def side_effect(args):
        if args == ["he","she","they","I","we"]:
            return "we"
        elif args == ["a","the"]:
            return "a"
    
    mock_random_choice = mocker.patch('build_sentences.random.choice', side_effect = side_effect)

    assert build_sentence(word, structure, data) == "We often run about an happy apples"

    mock_random_choice.assert_any_call(["he","she","they","I","we"])
    mock_random_choice.assert_any_call(["a","the"])