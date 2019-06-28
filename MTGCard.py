from datetime import datetime, date


class MTGCard:
    def __init__(self, name, release_date, oracle_text, set_name, url, id):
        self.name = name
        if isinstance(release_date, date):
            self.release_date = release_date
        else:
            self.release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
        self.oracle_text = oracle_text
        self.set_name = set_name
        self.url = url
        self.id = id


def parse_card_from_map(card_map):
    if 'oracle_text' in card_map:
        return MTGCard(card_map['name'], card_map['released_at'], card_map['oracle_text'], card_map['set'], card_map['scryfall_uri'], card_map['id'])
    return MTGCard(card_map['name'], card_map['released_at'], None, card_map['set'], card_map['scryfall_uri'], card_map['id'])
