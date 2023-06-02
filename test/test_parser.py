import os.path

from ..parser import extract_entries, is_answer, Entry


def test_is_answer():
    line = '\tThis is an answer'
    assert is_answer(line)


def test_is_answer_list():
    line = '* This is an answer'
    assert is_answer(line)


def test_is_answer_list_hyphen():
    line = '- This is an answer'
    assert is_answer(line)


def test_is_question():
    line = 'This is a question'
    assert not is_answer(line)


def test_extract_entries():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data', 'simple_questions.txt')
    answered, unanswered = extract_entries(filename)
    desired_answered_entry = Entry(question='What special python method implements addition?', answer='__add__')
    desired_unanswered_entry = Entry(question='This line contains nothing.', answer=None)

    assert len(answered) == 2
    assert len(unanswered) == 1
    assert desired_answered_entry in answered
    assert desired_unanswered_entry in unanswered