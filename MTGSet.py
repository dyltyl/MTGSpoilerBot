from datetime import datetime, date


class MTGSet:
    def __init__(self, name: str, code: str, release_date, card_count: int, set_type: str):
        self.name = name
        self.code = code
        print(type(release_date))
        if release_date is date:
            self.release_date = release_date
        else:
            self.release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
        self.card_count = card_count
        self.set_type = set_type


def parse_set_from_map(set_map) -> MTGSet:
    return MTGSet(set_map['name'], set_map['code'], set_map['released_at'], set_map['card_count'], set_map['set_type'])
