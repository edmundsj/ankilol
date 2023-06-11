import configparser
import logging
import os.path
import sys
from .parser import HTMLParser, TextParser, get_parser_class
from .writer import HTMLWriter, TextWriter, get_writer_class
from .anki import AnkiConnect
from .fetcher import GoogleDriveTransferManager, LocalTransferManager
from . import base_dir


def main(filename: str | None):
    logging.basicConfig(level=logging.INFO)
    anki_connect = AnkiConnect()

    if not anki_connect.is_running():
        logging.error('Cannot connect to Anki server. Have you tried starting it?')
        return

    config = configparser.ConfigParser()
    config.read(os.path.join(base_dir, 'config.ini'))

    if filename is None:
        transfer_manager = GoogleDriveTransferManager()
        doc_id = config.get('DEFAULT', 'main_doc_id')
    else:
        transfer_manager = LocalTransferManager()
        doc_id = filename

    content = transfer_manager.download_file(doc_id)
    temporary_filename = 'downloaded_doc.html'

    with open(temporary_filename, 'wb') as f:
        f.write(content)

    filename_base, extension = os.path.split(temporary_filename)
    Parser = get_parser_class(extension)
    Writer = get_writer_class(extension)

    parser = Parser(filename=temporary_filename)
    answered_entries, unanswered_entries = parser.extract_entries()

    if len(answered_entries) > 0:
        for entry in answered_entries:
            anki_connect.add_note(entry)
    anki_connect.sync()

    unanswered_filename = filename_base + '.unanswered' + extension
    writer = Writer(filename=unanswered_filename)
    writer.write(unanswered_entries)

    answered_filename = filename_base + '.answered' + extension
    writer = Writer(filename=answered_filename)
    writer.write(answered_entries)

    # Now, we modify in place the old learning document
    transfer_manager.upload_file(filename=unanswered_filename, file_id=doc_id)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 2:
        filename = sys.argv[1]
    else:
        filename = None
    main(filename=filename)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
