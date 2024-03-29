class MTGSet:
    def __init__(self, name, code, release_date, card_count, set_type):
        self.name = name
        self.code = code
        self.release_date = release_date
        self.card_count = card_count
        self.set_type = set_type

@staticmethod
def parse_set_from_map(set_map):
    return MTGSet(set_map['name'], set_map['code'], set_map['released_at'], set_map['card_count'], set_map['set_type'])
