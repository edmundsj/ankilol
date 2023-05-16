from collections import namedtuple
from typing import TextIO

Entry = namedtuple('Entry', ['question', 'answer'])


def write_entries(filename: str, entries: list[Entry]) -> None:
    with open(filename, 'w') as file:
        for entry in entries:
            write_entry(file, entry)


def write_entry(file: TextIO, entry: Entry):
    file.write(entry.question + '\n')
    if entry.answer is not None:
        file.write('\t' + entry.answer + '\n')


def extract_entries(filename: str) -> (list[Entry], list[Entry]):
    answered_questions = []
    unanswered_questions = []
    current_question = None

    num_lines = get_num_lines(filename)
    with open(filename, 'r') as file:
        for index, line in enumerate(file):
            is_last_line = index == num_lines - 1
            if line == '\n' and not is_last_line:
                continue
            if is_answer(line):
                new_entry = Entry(question=current_question, answer=parse_answer(line))
                answered_questions.append(new_entry)
                current_question = None
            else:
                if current_question is not None:
                    new_entry = Entry(question=current_question, answer=None)
                    unanswered_questions.append(new_entry)
                current_question = parse_question(line)

    return answered_questions, unanswered_questions


def is_answer(line: str) -> bool:
    if line.startswith('\t') or line.startswith('  '):
        return True
    else:
        return False


def get_num_lines(filename: str) -> int:
    with open(filename, 'r') as file:
        return sum(1 for line in file)


def parse_question(question: str) -> str:
    return question.removesuffix('\n')


def parse_answer(answer: str) -> str:
    return answer.removesuffix('\n').removeprefix('\t').strip(' ')
