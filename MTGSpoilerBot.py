import requests
import MTGSet
import MTGCard
from datetime import datetime


class MTGSpoilerBot:
    def __init__(self):
        self.current_sets = []
        self.current_cards = []

    def check_for_new_sets(self):
        self.get_all_sets()
        #Check the stored values and compare

    def check_for_new_cards(self):
        current_date = datetime.now().date()
        for mtg_set in self.current_sets:
            if mtg_set.release_date >= current_date and mtg_set.num_of_cards > 0:
                self.get_all_cards_in_set(mtg_set.code)

    def get_all_sets(self):
        r = requests.get('https://api.scryfall.com/sets')
        if r is None:
            print('Unable to get sets')
            return
        for mtg_set in r.json()['data']:
            self.current_sets.append(MTGSet.parse_set_from_map(mtg_set))

    def get_all_cards_in_set(self, set_code):
        r = requests.get('https://api.scryfall.com/cards/search?order=released&q=e%3A' + set_code + '&unique=prints')
        if r is None:
            print('Unable to get cards in: ' + set_code)
            return
        for card in r.json()['data']:
            self.current_cards.append(MTGCard.parse_card_from_map(card))


bot = MTGSpoilerBot()
bot.check_for_new_sets()
bot.check_for_new_cards()


