from tika import parser

raw = parser.from_file('C:\\Users\\InnSight\Documents\\Github\\Gloomhaven-Deck-Builder\\ghclass\\BT\\BT Cards.pdf')
print(raw['content'])