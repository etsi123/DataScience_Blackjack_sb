import pandas as pd
import numpy as np
from random import shuffle

class Blackjack_shoe:
    def __init__(self, num_decks_remaining,running_count,counting_rules,jackpot,expectation,\
                 avg_rt,lower_rt,upper_rt,small_cards):
        self.num_decks_remaining = num_decks_remaining
        self.running_count = running_count
        self.counting_rules = counting_rules
        self.shoe = []
        self.jackpot=jackpot
        self.avg_rt = avg_rt
        self.lower_rt=lower_rt
        self.upper_rt=upper_rt
        self.small_cards=small_cards
        self.expectation=expectation

    def create_shoe(self):
        """
        Parameters
        ----------
        num_decks : The Number of decks used to construct the shoe that will be played with. 
        This is chosen by the casino and fewer decks favors the player. 
        Returns
        -------
        shoe : The shuffled shoe. num_decks combined into one massive deck and shuffled. 
        """
        shoe = []
        for i in range(self.num_decks_remaining): 
            unique_cards = list(self.counting_rules.keys())
            shoe = shoe + unique_cards

        self.shoe=shoe
    
    def establish_count(self): 
        if self.running_count > self.num_decks_remaining*5*4: 
            raise Exception("Not possible to achieve this count")  
        for i in range(self.running_count): 
            ind = i % len(self.small_cards)
            card = self.small_cards[ind]
            self.shoe.remove(card)   
        shuffle(self.shoe)
        
    def get_shoe(self):
        return self.shoe
    def get_cards(self):
        return self.shoe[0],self.shoe[1],self.shoe[2],self.shoe[3]
    
    def evaluate_jackpot(self): 
        dc1,dc2,mc1,mc2 = self.shoe[0],self.shoe[1],self.shoe[2],self.shoe[3]
        if (dc1.split('_')[0] == 'ace') or (dc2.split('_')[0] == 'ace'):
            if dc1.split('_')[2] == dc2.split('_')[2] == mc1.split('_')[2] == mc2.split('_')[2]: 
                card_group = [dc1.split('_')[0],dc2.split('_')[0],mc1.split('_')[0],mc2.split('_')[0]]
                if sorted(card_group) == ['ace', 'jack', 'king', 'queen']: 
                    if dc1.split('_')[2] == 'diamonds': 
                        self.expectation = self.expectation+self.jackpot
                    else: 
                        self.expectation = self.expectation + self.jackpot/10        

    def get_expectation_ranges(self): 
        return self.expectation/self.upper_rt,self.expectation/self.avg_rt,self.expectation/self.lower_rt
    
    def summarize_results(self): 
        print('Average Expectation / hour is :' + str(self.expectation/self.avg_rt))
        print('Lower limit expectation / hour is :' + str(self.expectation/self.upper_rt))
        print('Upper limit expectation / hour is :' + str(self.expectation/self.lower_rt))
        