from pathlib import Path

from bs4 import BeautifulSoup, Tag
import typing
from abc import ABC
from typing import TextIO
from ankilol.definitions import Entry, HTML_ANSWER_OUTER_TAG, HTML_ANSWER_INNER_TAG


class GenericWriter(ABC):
    def __init__(self, filename: str | Path):
        pass
    def append(self, entries: list[Entry]):
        pass

    def write(self, entries: list[Entry]):
        pass


class HTMLWriter(GenericWriter):
    def __init__(self, filename: str | Path):
        self.filename = filename

    def write(self, entries):
        with open(self.filename, 'w+') as file:
            soup = BeautifulSoup(file, 'html.parser')
            self._initialize_document(soup)
            for entry in entries:
                question = self._create_question(entry)
                soup.body.append(question)
                if entry.answer is not None:
                    answer = self._create_answer(entry)
                    soup.body.append(answer)
            file.write(str(soup))

    def _initialize_document(self, soup: BeautifulSoup):
        html = soup.new_tag('html')
        head = soup.new_tag('head')
        title = soup.new_tag('title')
        body = soup.new_tag('body')
        soup.append(html)
        html.append(head)
        head.append(title)
        html.append(body)

    def _create_question(self, entry: Entry):
        soup = BeautifulSoup('', 'html.parser')
        question = soup.new_tag(name='p')
        question.string = entry.question
        return question

    def _create_answer(self, entry: Entry):
        soup = BeautifulSoup('', 'html.parser')
        answer = soup.new_tag(HTML_ANSWER_OUTER_TAG)
        content = soup.new_tag(HTML_ANSWER_INNER_TAG)
        content.string = entry.answer
        answer.append(content)
        return answer

    def _write_entry(self, file: TextIO, entry: Entry):
        file.write(entry.question + '\n')
        if entry.answer is not None:
            file.write('* ' + entry.answer + '\n')


class TextWriter(GenericWriter):
    def __init__(self, filename: str | Path):
        self.filename = filename

    def write(self, entries):
        with open(self.filename, 'w') as fh:
            for e in entries:
                self._write_entry(fh, e)

    def append(self, entries: list[Entry]):
        with open(self.filename, 'w+') as fh:
            for e in entries:
                self._write_entry(fh, e)
    def _write_entry(self, file: TextIO, entry: Entry):
        file.write(entry.question + '\n')
        if entry.answer is not None:
            file.write('* ' + entry.answer + '\n')


def get_writer_class(filename: str | Path) -> typing.Type[GenericWriter]:
    if '.html' in filename:
        return HTMLWriter
    elif '.txt' in filename:
        return TextWriter
    else:
        raise NotImplementedError('Only supported file extensions are .txt and .html')
