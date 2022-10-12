import os
import random
import argparse


class FlashCard:

    def __init__(self, card, definition, mistakes=0):
        self.card = card
        self.definition = definition
        self.mistakes = mistakes

    def __contains__(self, item):
        return item in self.definition

    def __eq__(self, other):
        if isinstance(other, str):
            return bool(self.definition == other)
        return False

    def __str__(self):
        return self.definition

    def save(self, file):
        print(self.card, self.definition, self.mistakes, file=file, sep=':', end='\n')

    def mistake(self):
        self.mistakes += 1


class FlashCards:

    def __init__(self, import_file=None, export_file=None):
        self.dictionary = dict()
        self.logger = list()
        self.export_file = export_file
        if import_file is not None:
            self.import_(import_file)

    def key_by_value(self, value):
        return list(self.dictionary.keys())[list(self.dictionary.values()).index(value)]

    def add(self):
        card = self.input('The card:\n')
        while card in self.dictionary.keys():
            card = self.input(f'The card "{card}" already exists. Try again:\n')

        definition = self.input('The definition of the card:\n')
        while definition in self.dictionary.values():
            definition = self.input(f'The definition "{definition}" already exists. Try again:\n')

        self.dictionary[card] = FlashCard(card, definition)
        self.print(f'The pair ("{card}":"{definition}") has been added.\n')

    def remove(self):
        card = self.input('Which card?\n')
        if card in self.dictionary.keys():
            self.dictionary.pop(card)
            self.print("The card has been removed.\n")
        else:
            self.print(f"""Can't remove "{card}": there is no such card.\n""")

    def import_(self, file_name=None):
        if file_name is None:
            file_name = self.input('File name:\n')

        if not os.path.exists(file_name):
            self.print('FIle not found.\n')
            return

        file = open(file_name, 'r')
        dictionary_to_append = dict()
        line = file.readline()
        while line != '':
            card, definition, mistakes = line.split(':')
            dictionary_to_append[card] = FlashCard(card, definition, int(mistakes))
            line = file.readline()

        self.dictionary.update(dictionary_to_append)
        self.print(f'{len(dictionary_to_append)} cards have been loaded.\n')

    def export_(self, file_name=None):
        if file_name is None:
            file_name = self.input('File name:\n')

        with open(file_name, 'w') as f:
            for flash_card in self.dictionary.values():
                flash_card.save(f)
        self.print(f'{len(self.dictionary)} cards have been saved.')

    def ask(self):
        amount = int(self.input('How many times to ask?\n'))

        for _ in range(amount):
            card = random.choice(list(self.dictionary.keys()))
            user_def = self.input(f'Print the definition of "{card}":\n')

            if user_def == self.dictionary[card]:
                self.print('Correct')
                continue

            self.dictionary[card].mistake()
            if user_def in self.dictionary.values():
                self.print(f'Wrong. The right answer is "{self.dictionary[card]}", but your definition is correct for "{self.key_by_value(user_def)}"')
            else:
                self.print(f'Wrong. The right answer is "{self.dictionary[card]}"')

        self.print()

    def log(self):
        file_name = self.input('File name:\n')

        with open(file_name, 'w') as f:
            for log in self.logger:
                print(log, file=f)
        self.print('The log has been saved.')

    def hardest_card(self):
        hardest_cards, most_mistakes = list(), 0

        for card in self.dictionary.values():
            if card.mistakes == most_mistakes:
                hardest_cards.append(card.card)
            elif card.mistakes > most_mistakes:
                most_mistakes = card.mistakes
                hardest_cards = [card.card]

        if most_mistakes == 0:
            self.print('There are no cards with errors.\n')
        elif len(hardest_cards) == 1:
            self.print(f'The hardest card is "{hardest_cards}". You have {most_mistakes} errors answering it.\n')
        else:
            self.print(f"""The hardest cards are "{", ".join(hardest_cards)}".\n""")

    def reset_stats(self):
        for card in self.dictionary.values():
            card.mistakes = 0
        self.print('Card Statistics have been reset.')

    def print(self, value=''):
        self.logger.append(value)
        print(value)

    def input(self, comment=''):
        self.logger.append(comment)
        value = input(comment)
        self.logger.append(value)
        return value

    def exit_(self):
        if self.export_file is not None:
            self.export_(self.export_file)
        self.print('Bye bye!')
        exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--import_from", default=None)
    parser.add_argument("--export_to", default=None)

    args = parser.parse_args()
    flash_cards = FlashCards(import_file=args.import_from, export_file=args.export_to)

    commands = {
                'add':          flash_cards.add,
                'remove':       flash_cards.remove,
                'import':       flash_cards.import_,
                'export':       flash_cards.export_,
                'ask':          flash_cards.ask,
                'exit':         flash_cards.exit_,
                'log':          flash_cards.log,
                'hardest card': flash_cards.hardest_card,
                'reset stats':  flash_cards.reset_stats
                }

    while True:
        user_input = flash_cards.input(f'Input The action ({", ".join(commands.keys())}):\n')
        commands[user_input]()


if __name__ == '__main__':
    main()
