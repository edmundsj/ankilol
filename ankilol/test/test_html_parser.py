import os.path
import pytest

from ..parser import (
    GenericParser, TextParser, HTMLParser, inner_content, get_tags_text, get_tags_html, strip_tags_text, strip_tags_html
)
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


@pytest.mark.parametrize(
    'html,output',
    [
        ('<p>Hello there</p>', '<p>Hello there</p>'),
        ('<div><p>Hello there</p></div>', '<p>Hello there</p>'),
        ('<div><p>Hello <b>hi</b> there</p></div>', '<p>Hello <b>hi</b> there</p>'),
    ]
)
def test_inner_element_extract(html, output):
    content = BeautifulSoup(html, 'html.parser')
    parsed_content = inner_content(content)
    assert str(parsed_content) == str(output)


@pytest.mark.parametrize(
    'text,output',
    [
        ('#tag1, hello #tag2', ['#tag1', '#tag2']),
        ('#tag1', ['#tag1']),
        ('tag1', []),
    ]
)
def test_get_tags_text(text, output):
    tags = get_tags_text(text)
    assert tags == output


@pytest.mark.parametrize(
    'text,output',
    [
        ('#tag1, hello #tag2', 'hello'),
        ('#tag1, hello #tag2 there', 'hello there'),
        ('#tag1', ''),
        ('tag1', 'tag1'),
    ]
)
def test_strip_tags_text(text, output):
    actual_text = strip_tags_text(text)
    assert actual_text == output


@pytest.mark.parametrize(
    'html,output',
    [
        ('<p>#tag1, hello #tag2</p>', ['#tag1', '#tag2']),
        ('<p>#tag1, hello #tag2 there</p>', ['#tag1', '#tag2']),
        ('<p>#tag1</p>', ['#tag1']),
    ]
)
def test_get_tags_html(html, output):
    content = BeautifulSoup(html, 'html.parser')
    tags = get_tags_html(content)
    assert tags == output


@pytest.mark.parametrize(
    'html,output',
    [
        ('<p>#tag1, hello #tag2</p>', '<p>hello</p>'),
        ('<p>#tag1, hello #tag2 there</p>', '<p>hello there</p>'),
        ('<p>#tag1</p>', '<p></p>'),
    ]
)
def test_strip_tags_html(html, output):
    content = BeautifulSoup(html, 'html.parser')
    actual_content = strip_tags_html(content)
    assert str(actual_content) == output



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
        question='<span>Who said “software’s primary technical imperative is minimizing complexity”?</span>',
        answer='<span>Steve McConnel of Code Complete</span>')
    desired_unanswered_entry = Entry(
        question='<span>Are Google test suites compiled into a '
        'binary and then run as a standalone executable, or do they interact with another executable?</span>',
        answer=None)

    assert len(answered) == 4
    assert desired_answered_entry in answered

    assert len(unanswered) == 11
    assert desired_unanswered_entry in unanswered



def test_parse_question_with_tag(html_parser, soup):
    html = '''<p style="color: red">Item 1 is <b>bold</b> and has an [element]</p>'''
    content = BeautifulSoup(html, 'html.parser')
    parsed_question = html_parser._parse_question(content)
    desired_question = '''<p>Item 1 is <b>bold</b> and has an [element]</p>'''
    assert parsed_question == desired_question
