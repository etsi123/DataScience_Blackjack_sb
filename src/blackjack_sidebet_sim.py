import pandas as pd
import numpy as np
from random import shuffle
import math

class Blackjack_shoe:
    def __init__(self, num_decks_remaining,running_count,counting_rules,\
                 small_cards,win_counter):
        self.num_decks_remaining = num_decks_remaining
        self.running_count = running_count
        self.counting_rules = counting_rules
        self.shoe = []
        self.small_cards=small_cards
        self.win_counter = win_counter

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
        """
        This functioin establishes the specified count by removing cards from the shoe to achieve this goal. 
        Currently setup for positive counts, which is what we want in virtually all cases. 
        """
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
        """
        Function to evaluate whether or not the jackpot was achieved. 
        """
        dc1,dc2,mc1,mc2 = self.shoe[0],self.shoe[1],self.shoe[2],self.shoe[3]
        if (dc1.split('_')[0] == 'ace') or (dc2.split('_')[0] == 'ace'):
            if dc1.split('_')[2] == dc2.split('_')[2] == mc1.split('_')[2] == mc2.split('_')[2]: 
                card_group = [dc1.split('_')[0],dc2.split('_')[0],mc1.split('_')[0],mc2.split('_')[0]]
                if sorted(card_group) == ['ace', 'jack', 'king', 'queen']: 
                    self.win_counter = self.win_counter + 1     

    def get_expectation_ranges(self): 
        return self.win_counter
    
    def summarize_results(self): 
        """
        Function to summarize how the simulation went for a specific running count / number of decks remaining 
        combination. 
        """
        print('Num Decks Remaining is ' + str(self.num_decks_remaining))
        print('Running Count is ' + str(self.running_count))
        print('Number of wins is ' + str(self.win_counter))
    
    def simulate_blackjack_shoe(self,deck_penetration):
        """
        Simulate a blackjack shoe and record frequency of specific running coount/number of decks remaining
        combinations. 
        """
        shuffle(self.shoe)
        sol = []
        numcards = len(self.shoe)
        cut_card = int(numcards*deck_penetration)
        running_count = 0
        num_decks_remaining = len(self.shoe) / 52
        while len(self.shoe) >= (numcards - cut_card): 
            for i in range(0,10): #10 cards per round 
                card = self.shoe.pop(0)
                running_count = running_count + self.counting_rules[card] 
            num_decks_remaining = math.ceil(len(self.shoe)/52)
            sol.append([num_decks_remaining,running_count])
        return sol



