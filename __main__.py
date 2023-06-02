import logging
import sys
from .parser import extract_entries, write_entries
from .connector import add_note, is_anki_running


def main(filename: str):
    logging.basicConfig(level=logging.INFO)
    # Use a breakpoint in the code line below to debug your script.
    if not is_anki_running():
        logging.error('Cannot connect to Anki server. Have you tried starting it?')
        return
    answered_entries, unanswered_entries = extract_entries(filename)
    write_entries(filename='remaining_questions.txt', entries=unanswered_entries)
    if len(answered_entries) > 0:
        for entry in answered_entries:
            add_note(entry)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(filename=sys.argv[1])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
