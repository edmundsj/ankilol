import os.path
import pytest

from ..parser import TextParser
from definitions import Entry


@pytest.fixture
def text_parser() -> TextParser:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data', 'simple_questions.txt')
    yield TextParser(filename=filename)


def test_is_answer(text_parser):
    line = '\tThis is an answer'
    assert text_parser._is_answer(line)


def test_is_answer_list(text_parser):
    line = '* This is an answer'
    assert text_parser._is_answer(line)


def test_is_answer_list_hyphen(text_parser):
    line = '- This is an answer'
    assert text_parser._is_answer(line)


def test_is_question(text_parser):
    line = 'This is a question'
    assert not text_parser._is_answer(line)


def test_extract_entries_text(text_parser):
    answered, unanswered = text_parser.extract_entries()
    desired_answered_entry = Entry(question='What special python method implements addition?', answer='__add__')
    desired_unanswered_entry = Entry(question='This line contains nothing.', answer=None)

    assert len(answered) == 2
    assert desired_answered_entry in answered

    assert len(unanswered) == 1
    assert desired_unanswered_entry in unanswered
