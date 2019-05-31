from tika import parser

raw = parser.from_file('C:\\Users\\InnSight\Documents\\Github\\Gloomhaven-Deck-Builder\\ghclass\\BR\\BR Cards.pdf')
content = raw['content'].split('Brute\n')
n = 5
list(filter(None, content[17].split('\n')))

