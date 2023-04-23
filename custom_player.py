import random

from poker_squares_utils import *

class RandomPlayer:
    def __init__(self):
        self.name='RandomPlayer'
        self.pre_defined_cards_loc=[(i,j) for i in range(5) for j in range(5)]
        self.move_num=0
        random.shuffle(self.pre_defined_cards_loc)
    def move(self,card,remaining_time):
        row,col=self.pre_defined_cards_loc[self.move_num]
        self.move_num+=1
        return row,col

class PMCTSPlayer:
    pass






