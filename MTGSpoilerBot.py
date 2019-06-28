import requests
import MTGSet
import MTGCard
from datetime import datetime
from typing import List
from Database import Database


class MTGSpoilerBot:
    def __init__(self):
        self.current_sets = []
        self.current_cards = []
        self.all_sets = []
        self.all_cards = []
        self.database = Database()

    def check_for_new_sets(self):
        self.current_sets = self.database.get_sets()
        self.all_sets = MTGSpoilerBot.get_all_sets()
        if len(self.current_sets) != len(self.all_sets):
            new_sets = []
            for mtg_set in self.all_sets:
                if mtg_set not in self.current_sets:
                    new_sets.append(mtg_set)
            self.database.insert_sets(new_sets)
            return new_sets
        return []

    def check_for_new_cards(self): #TODO: Fix all this
        current_date = datetime.now().date()
        new_cards = []
        for mtg_set in self.current_sets:
            if mtg_set.release_date >= current_date and mtg_set.card_count > 0:
                scryfall_cards = self.get_all_cards_in_set(mtg_set.code)
                db_cards = self.database.get_cards_from_set(mtg_set.code)
                if len(db_cards) != len(scryfall_cards):
                    for card in scryfall_cards:
                        if card not in db_cards:
                            new_cards.append(card)
        self.database.insert_cards(new_cards)
        return new_cards


    @staticmethod
    def get_all_sets() -> List[MTGSet]:
        r = requests.get('https://api.scryfall.com/sets')
        if r is None:
            print('Unable to get sets')
            return []
        mtg_sets = []
        for mtg_set in r.json()['data']:
            mtg_sets.append(MTGSet.parse_set_from_map(mtg_set))
        return mtg_sets

    @staticmethod
    def get_all_cards_in_set(set_code) -> List[MTGCard]:
        r = requests.get('https://api.scryfall.com/cards/search?order=released&q=e%3A' + set_code + '&unique=prints')
        if r is None:
            print('Unable to get cards in: ' + set_code)
            return []
        cards = []
        for card in r.json()['data']:
            cards.append(MTGCard.parse_card_from_map(card))
        return cards


