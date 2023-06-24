import typing
from pathlib import Path
from typing import Callable, Any
from abc import ABC
from copy import copy
from functools import lru_cache

import bs4
from bs4 import BeautifulSoup

from ankilol.definitions import Entry, HTML_ANSWER_OUTER_TAG


class GenericParser(ABC):
    def __init__(self, filename: str | Path):
        pass

    def extract_entries(self)-> (list[Entry], list[Entry]):
        pass


def extract_entries(
        iterable,
        is_answer: Callable[[Any], bool],
        parse_question: Callable[[Any], Any],
        parse_answer: Callable[[Any], Any],
) -> (list[Entry], list[Entry]):
    answered_questions = []
    unanswered_questions = []
    current_question = None

    for index, line in enumerate(iterable):
        is_last_line = index == len(iterable) - 1
        if is_answer(line):
            new_entry = Entry(question=current_question, answer=parse_answer(line), tags=[])
            answered_questions.append(new_entry)
            current_question = None
        elif not is_answer(line) and not is_last_line:
            if current_question is not None:
                new_entry = Entry(question=current_question, answer=None, tags=[])
                unanswered_questions.append(new_entry)
            current_question = parse_question(line)
        elif not is_answer(line) and is_last_line:
            new_entry = Entry(question=parse_question(line), answer=None, tags=[])
            unanswered_questions.append(new_entry)

    return answered_questions, unanswered_questions


class HTMLParser(GenericParser):
    def __init__(self, filename: str):
        self.filename = filename

    def extract_entries(self) -> (list[Entry], list[Entry]):
        with open(self.filename, 'r') as fh:
            soup = BeautifulSoup(fh, 'html.parser')
            body = soup.body
            entries = []
            if body is not None:
                entries = [element for element in body.find_all(recursive=False)]
            return extract_entries(entries, self._is_answer, self._parse_question, self._parse_answer)
        pass

    def _is_answer(self, line: bs4.Tag):
        if line.name == HTML_ANSWER_OUTER_TAG:
            return True
        return False

    def _parse_question(self, element: bs4.Tag):
        question = inner_content(element)
        question.attrs.clear()
        return str(question)

    def _parse_answer(self, element: bs4.Tag):
        answer = inner_content(element)
        answer.attrs.clear()
        return str(answer)


class TextParser(GenericParser):
    ANSWER_PREFIXES = ['\t', '  ', '* ']

    def __init__(self, filename: str):
        self.filename = filename

    def extract_entries(self) -> (list[Entry], list[Entry]):
        with open(self.filename, 'r') as file:
            lines = [line for line in file if line != '\n']
            return extract_entries(lines, self._is_answer, self._parse_question, self._parse_answer)

    def _is_answer(self, line: str) -> bool:
        valid_starts = ['\t', '  ', '* ', '-']
        if any([line.startswith(start) for start in valid_starts]):
            return True
        else:
            return False

    def _parse_question(self, question: str) -> str:
        return question.removesuffix('\n')

    def _parse_answer(self, answer: str) -> str:
        stripped_answer = answer
        for prefix in self.ANSWER_PREFIXES:
            stripped_answer = stripped_answer.removeprefix(prefix)
        return stripped_answer.removesuffix('\n')


def get_parser_class(filename: str | Path) -> typing.Type[GenericParser]:
    if '.html' in filename:
        return HTMLParser
    elif '.txt' in filename:
        return TextParser
    else:
        raise NotImplementedError('Only supported file extensions are .txt and .html')


def inner_content(outer: bs4.Tag):
    if len(outer.contents) > 1 or isinstance(outer.contents[0], str):
        return copy(outer)
    else:
        return inner_content(outer.contents[0])

def get_tags_html(inner_element: bs4.Tag) -> list[str]:
    tags, _= parse_tags_html(inner_element)
    return tags


def strip_tags_html(inner_element: bs4.Tag) -> bs4.Tag:
    _, new_element = parse_tags_html(inner_element)
    return new_element


@lru_cache(maxsize=None)
def parse_tags_html(element: bs4.Tag) -> (bs4.Tag, list[str]):
    tags = []
    soup = BeautifulSoup('', 'html.parser')
    inner_elem = inner_content(element)
    new_inner_elem = soup.new_tag(name=inner_elem.name)

    for elem in inner_elem:
        if isinstance(elem, str):
            new_tags, remaining_string = parse_tags_text(elem)
            tags.extend(new_tags)
            string_node = soup.new_string(remaining_string)
            new_inner_elem.append(string_node)
        else:
            new_inner_elem.append(elem)

    return (tags, new_inner_elem)


@lru_cache(maxsize=None)
def parse_tags_text(text: str) -> (str, list[str]):
    words = text.split()
    tags = [word for word in words if word.startswith('#')]
    tags = [tag.strip(',') for tag in tags]
    non_tags = [word for word in words if not word.startswith('#')]
    output_string =  ' '.join(non_tags)
    return (tags, output_string)


def get_tags_text(text: str) -> list[str]:
    tags, _ = parse_tags_text(text)
    return tags


def strip_tags_text(text: str) -> str:
    _, output_string = parse_tags_text(text)
    return output_string

