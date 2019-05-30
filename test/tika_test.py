from tika import parser

raw = parser.from_file('C:\\Users\\InnSight\Documents\\Github\\Gloomhaven-Deck-Builder\\BT Cards.pdf')
print(raw['content'])