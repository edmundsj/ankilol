import typing
from collections import namedtuple
from typing import TextIO, Callable, Any, TypeVar, Generic
from abc import ABC

import bs4
from bs4 import BeautifulSoup

Entry = namedtuple('Entry', ['question', 'answer'])


class GenericParser(ABC):
    def write_entries(self, entries: list[Entry]):
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
            new_entry = Entry(question=current_question, answer=parse_answer(line))
            answered_questions.append(new_entry)
            current_question = None
        elif not is_answer(line) and not is_last_line:
            if current_question is not None:
                new_entry = Entry(question=current_question, answer=None)
                unanswered_questions.append(new_entry)
            current_question = parse_question(line)
        elif not is_answer(line) and is_last_line:
            new_entry = Entry(question=parse_question(line), answer=None)
            unanswered_questions.append(new_entry)

    return answered_questions, unanswered_questions


class HTMLParser(GenericParser):
    def __init__(self, filename: str):
        self.filename = filename

    def write_entries(self, entries: list[Entry]):
        pass

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
        if line.name == 'ul':
            return True
        return False

    def _parse_question(self, element: bs4.Tag):
        return element.text

    def _parse_answer(self, element: bs4.Tag):
        return element.text


class TextParser(GenericParser):
    ANSWER_PREFIXES = ['\t', '  ', '* ']

    def __init__(self, filename: str):
        self.filename = filename

    def write_entries(self, entries: list[Entry]) -> None:
        with open(self.filename, 'w') as file:
            for entry in entries:
                self._write_entry(file, entry)

    def extract_entries(self) -> (list[Entry], list[Entry]):
        with open(self.filename, 'r') as file:
            lines = [line for line in file if line != '\n']
            return extract_entries(lines, self._is_answer, self._parse_question, self._parse_answer)

    def _write_entry(self, file: TextIO, entry: Entry):
        file.write(entry.question + '\n')
        if entry.answer is not None:
            file.write('\t' + entry.answer + '\n')

    def _is_answer(self, line: str) -> bool:
        valid_starts = ['\t', '  ', '* ', '-']
        if any([line.startswith(start) for start in valid_starts]):
            return True
        else:
            return False

    def _get_num_lines(self) -> int:
        with open(self.filename, 'r') as file:
            return sum(1 for line in file)

    def _parse_question(self, question: str) -> str:
        return question.removesuffix('\n')

    def _parse_answer(self, answer: str) -> str:
        stripped_answer = answer
        for prefix in self.ANSWER_PREFIXES:
            stripped_answer = stripped_answer.removeprefix(prefix)
        return stripped_answer.removesuffix('\n')
