from writer import HTMLWriter
from definitions import Entry
import os


def test_write_single_question(tmp_path):
    file_to_write = tmp_path / "test.html"
    writer = HTMLWriter(file_to_write)
    entry = Entry(question='test question', answer=None)
    entries = [entry]
    writer.write(entries)
    assert os.path.exists(file_to_write)
    with open(file_to_write, 'r') as file:
        content = file.read()
        assert 'test question' in content


def test_write_single_question_answer(tmp_path):
    file_to_write = tmp_path / "test.html"
    writer = HTMLWriter(file_to_write)
    entry = Entry(question='test question', answer='test answer')
    entries = [entry]
    writer.write(entries)
    assert os.path.exists(file_to_write)
    with open(file_to_write, 'r') as file:
        content = file.read()
        assert 'test question' in content
        assert 'test answer' in content

