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
    def __init__(self):
         self.point_system= PointSystem()
         self.move_num = 0
         self.name = 'PMCTSPlayer'
         self.empty_homes=set([(i, j) for i in range(5) for j in range(5)])
         self.rem_cards=set(Deck.get_all_cards())
         self.board=[[None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None], ]

    def simulate(self,board, rem_cards, depth=None):
        new_board = [[None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None], ]
        rem_cards = Deck.clone_cards(rem_cards)
        Deck.shuffle(rem_cards)
        card_pointer = 0
        num_fill_homes=len(self.empty_homes)
        for i in range(5):
            for j in range(5):
                if board[i][j] is not None:
                    new_board[i][j] = board[i][j].__copy__()
                    num_fill_homes-=1
                else:
                    if (depth is None) or (card_pointer < depth):
                        new_board[i][j] = rem_cards[card_pointer].__copy__()
                        card_pointer += 1
                if num_fill_homes==0 and (depth is not None and card_pointer>=depth):
                    return new_board
        return new_board

    def n_simulate(self,board, rem_cards, depth=None, n=1):
        points=0
        for i in range(n):
            b = self.simulate(board, rem_cards, depth)
            points+=self.point_system.get_board_score(b)
        points=points/n
        return points

    def move(self,card,remaining_time):
        if len(self.empty_homes)==1:
            i,j=self.empty_homes.pop()
            return i,j

        self.rem_cards.remove(card)

        best_move_i=None
        best_move_j=None
        best_utility=None

        for i,j in self.empty_homes:
             self.board[i][j]=card
             utility=self.n_simulate(self.board,self.rem_cards,None,100)
             if (best_utility is None) or (utility>best_utility):
                 best_utility=utility
                 best_move_i=i
                 best_move_j=j
             self.board[i][j]=None

        self.board[best_move_i][best_move_j]=card
        self.empty_homes.remove((best_move_i,best_move_j))
        self.move_num+=1
        return best_move_i,best_move_j


    def __init__(self):
         self.point_system= PointSystem()
         self.move_num = 0
         self.name = 'PMCTSPlayer'
         self.empty_homes=set([(i, j) for i in range(5) for j in range(5)])
         self.rem_cards=set(Deck.get_all_cards())
         self.board=[[None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None], ]

    def simulate(self,board, rem_cards, depth=None):
        new_board = Board.clone_board(board)
        rem_cards = Deck.clone_cards(rem_cards)
        Deck.shuffle(rem_cards)
        card_pointer = 0
        num_fill_homes=len(self.empty_homes)
        empty_homes=set(self.empty_homes)
        if depth is None or depth>len(empty_homes):
            depth=len(empty_homes)
        for d in range(depth):
            c=rem_cards.pop()
            i,j=self.find_move_with_highest_immediate_reward(board,c,empty_homes)
            new_board[i][j]=c
            empty_homes.remove((i,j))
        return new_board

    def n_simulate(self,board, rem_cards, depth=None, n=1):
        points=0
        for i in range(n):
            b = self.simulate(board, rem_cards, depth)
            points+=self.point_system.get_board_score(b)
        points=points/n
        return points

    def move(self,card,remaining_time):
        if len(self.empty_homes)==1:
            i,j=self.empty_homes.pop()
            return i,j

        self.rem_cards.remove(card)

        best_move_i=None
        best_move_j=None
        best_utility=None

        for i,j in self.empty_homes:
             self.board[i][j]=card
             utility=self.n_simulate(self.board,self.rem_cards,None,20)
             if (best_utility is None) or (utility>best_utility):
                 best_utility=utility
                 best_move_i=i
                 best_move_j=j
             self.board[i][j]=None

        self.board[best_move_i][best_move_j]=card
        self.empty_homes.remove((best_move_i,best_move_j))
        self.move_num+=1
        return best_move_i,best_move_j

    def find_move_with_highest_immediate_reward(self,board,card,empty_homes):
        best_move_i=None
        best_move_j=None
        best_utility=None

        base_util=self.point_system.get_board_score(board)

        for i,j in empty_homes:
            board[i][j]=card
            utility=self.point_system.get_board_score(board)
            if (best_utility is None) or (utility > best_utility):
                best_utility = utility
                best_move_i = i
                best_move_j = j
            self.board[i][j] = None

        if best_utility==base_util:
            lst = list(empty_homes)
            random.shuffle(lst)
            best_move_i ,best_move_j = lst[0]


        return best_move_i,best_move_j






