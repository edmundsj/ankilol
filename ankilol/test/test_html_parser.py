import os.path
import pytest

from ..parser import GenericParser, TextParser, HTMLParser
from definitions import Entry
from bs4 import BeautifulSoup

@pytest.fixture
def html_parser() -> HTMLParser:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data', 'html_questions.html')
    yield HTMLParser(filename=filename)


@pytest.fixture
def soup() -> BeautifulSoup:
    yield BeautifulSoup('', 'html.parser')


def test_is_answer_list(html_parser, soup):
    line = soup.new_tag(name='ul')
    li = soup.new_tag(name='li')
    li.string = 'This is an answer'
    line.append(li)

    assert html_parser._is_answer(line)


def test_is_question(html_parser, soup):
    line = soup.new_tag(name='p')
    line.string = 'this is a question'

    assert not html_parser._is_answer(line)


def test_extract_entries_html(html_parser, soup):
    answered, unanswered = html_parser.extract_entries()
    desired_answered_entry = Entry(
        question='Who said “software’s primary technical imperative is minimizing complexity”?',
        answer='Steve McConnel of Code Complete')
    desired_unanswered_entry = Entry(
        question='Are Google test suites compiled into a '
        'binary and then run as a standalone executable, or do they interact with another executable?',
        answer=None)

    assert len(answered) == 4
    assert desired_answered_entry in answered

    assert len(unanswered) == 11
    assert desired_unanswered_entry in unanswered


def test_parse_question(html_parser, soup):
    line = soup.new_tag(name='p')
    content = 'this is <b>a</b> question'
    line.string = content
    parsed_question = html_parser._parse_question(line)
    assert parsed_question == content
