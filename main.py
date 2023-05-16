import sys
from .parser import extract_entries, write_entries
from .connector import add_note


def main(filename: str):
    # Use a breakpoint in the code line below to debug your script.
    answered, unanswered = extract_entries(filename)
    write_entries(filename='remaining_questions.txt', entries=unanswered)
    if len(answered) > 0:
        add_note(answered[0])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(filename=sys.argv[1])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
