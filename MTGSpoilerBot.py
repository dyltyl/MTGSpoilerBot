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
        self.database = Database()
        self.current_date = datetime.now().date()

    def check_for_new_sets(self):
        self.current_sets = []
        db_sets = self.database.get_sets()
        all_sets = MTGSpoilerBot.get_all_sets()
        if len(db_sets) != len(all_sets):
            new_sets = []
            for mtg_set in all_sets:
                if mtg_set not in db_sets:
                    new_sets.append(mtg_set)
                if mtg_set.release_date >= self.current_date:
                    self.current_sets.append(mtg_set)
            self.database.insert_sets(new_sets)
            return new_sets
        return []

    def check_for_new_cards(self):
        new_cards = []
        print('There are ' + str(len(self.current_sets)) + ' in the db')
        for mtg_set in self.current_sets:
            if mtg_set.release_date >= self.current_date and mtg_set.card_count > 0:
                scryfall_cards = self.get_all_cards_in_set(mtg_set.code)
                db_cards = self.database.get_cards_from_set(mtg_set.code)
                if len(db_cards) != len(scryfall_cards):
                    for card in scryfall_cards:
                        if card not in db_cards:
                            new_cards.append(card)
            else:
                print(mtg_set.code + ' not a current set')
        self.database.insert_cards(new_cards)
        return new_cards


    @staticmethod
    def get_all_sets():
        r = requests.get('https://api.scryfall.com/sets')
        if r is None:
            print('Unable to get sets')
            return []
        mtg_sets = []
        for mtg_set in r.json()['data']:
            mtg_sets.append(MTGSet.parse_set_from_map(mtg_set))
        return mtg_sets

    @staticmethod
    def get_all_cards_in_set(set_code):
        r = requests.get('https://api.scryfall.com/cards/search?order=released&q=e%3A' + set_code + '&unique=prints')
        if r is None:
            print('Unable to get cards in: ' + set_code)
            return []
        cards = []
        for card in r.json()['data']:
            cards.append(MTGCard.parse_card_from_map(card))
        return cards


