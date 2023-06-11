# Anki Card Knowledge Syncer

## The Problem
I like to ask lots of questions, but I can't always immediately find out the answers to those questions. So I store them in a google doc. When I do figure out the answers, I add them. Now, I would like to take that question/answer pair and create an Anki flashcard, so that I can store it in my long-term memory. However, copy-pasting these questions and answers into anki is a time-consuming process, and one which can be fully automated. 

## The solution
This project takes a formatted set of questions and answers stored as a cloud document, creates flashcards from those question/answer pairs, adds them to an Anki deck, and syncs that local deck with AnkiWeb. 

## Example usage with locally-downloaded HTML files
```
python -m card_parser input_file.html
```

## Example usage with locally-downloaded text files
```
python -m card_parser input_file.txt
```

## Example usage with files stored on google drive
### Prerequisites
#. Sign up for a google cloud account
#. Create a new project and service account for that project
#. Share the document with the service account's e-mail
#. Download the service account's .json credentials and place in `service_account.json` file in `card_parser` directory
#. Setup config.ini to point to the appropriate google doc ID

Then, just run the following command:
```
python -m card_parser
```

Your document should have been uploaded in-place.

## Disclaimer
NOTE: This package is currently under development, and has not yet been published to pip. The only current way to install it is through cloning this repository.
