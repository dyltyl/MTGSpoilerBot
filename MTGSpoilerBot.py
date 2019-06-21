import requests
import MTGSet


class MTGSpoilerBot:
    def __init__(self):
        self.current_sets = []

    def check_for_new_sets(self):
        self.get_all_sets()
        #Check the stored values and compare

    def get_all_sets(self):
        r = requests.get('https://api.scryfall.com/sets?pretty')
        if r is None:
            print('Unable to get sets')
            return
        for x in r.json()['data']:
            self.current_sets.append(MTGSet.parse_set_from_map(x))


