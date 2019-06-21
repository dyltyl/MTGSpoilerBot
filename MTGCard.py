from datetime import datetime
class MTGCard:
    def __init__(self, name, release_date, oracle_text, set_name, url):
        self.name = name
        self.release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
        self.oracle_text = oracle_text
        self.set_name = set_name
        self.url = url


def parse_card_from_map(card_map):
    if 'oracle_text' in card_map:
        return MTGCard(card_map['name'], card_map['released_at'], card_map['oracle_text'], card_map['set'], card_map['scryfall_uri'])
    return MTGCard(card_map['name'], card_map['released_at'], None, card_map['set'], card_map['scryfall_uri'])
