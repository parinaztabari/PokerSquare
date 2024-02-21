import random
from statistics import mean,stdev
import time
import multiprocessing
from custom_player import *

class Card:
    rank_to_value={"A":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10, "J":11, "Q":12, "K":13}

    def __init__(self,suite,rank):
        self.suite=suite
        self.rank=rank

    def __repr__(self):
        return f"{self.rank}{self.suite}"

    def __eq__(self, other):
        if self.suite==other.suite and self.rank==other.rank: return True
        return False

    def __copy__(self):
        return Card(self.suite,self.rank)

    def __hash__(self):
        return hash(self.__repr__())

class Deck:
    @staticmethod
    def get_all_cards():
        return [Card(s,r)
           for s in ["C", "D", "H", "S"]
           for r in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]]

    @staticmethod
    def clone_cards(cards):
        return [c.__copy__() for c in cards]

    @staticmethod
    def shuffle(cards,random_state=None):
        if random_state is not None:random.seed(random_state)
        random.shuffle(cards)
        return cards

class Board:

    @staticmethod
    def create_random_board(num_empty_homes=2,random_state=None):
        cards = Deck.shuffle(Deck.get_all_cards(),random_state=random_state)
        if random_state is not None:random.seed(random_state)
        empty_homes = random.sample(range(25), num_empty_homes)
        board = [[cards[i * 5 + k] if i * 5  + k not in empty_homes else None for k in range(5)] for i in range(5)]
        return board

    @staticmethod
    def print_board(board):
        for i in range(5):
            for j in range(5):
                print(f"{ '--' if board[i][j] is None else board[i][j]}",end='  ')
            print(end='\n')
        print(end='\n')

    @staticmethod
    def clone_board(board):
        new_board=[]
        for i in range(5):
            row=[]
            for j in range(5):
                row.append(None if board[i][j] is None else board[i][j].__copy__())
            new_board.append(row)
        return new_board

class Hand:
    Hand_Id_to_Category_Map={1:'Royal_Flush',2:'Straight_Flush',3:'Four_Of_A_Kind',4:'Full_House',
                             5:'Flush',6:'Straight',7:'Three_Of_A_Kind',8:'Two_Pair',9:'One_Pair',
                             10:'High_Card'}
    Royal_Flush=1
    Straight_Flush = 2
    Four_Of_A_Kind=3
    Full_House=4
    Flush=5
    Straight = 6
    Three_Of_A_Kind=7
    Two_Pair=8
    One_Pair=9
    High_Card=10

    hands_idx = [[(i, k) if i <= 4 else (k, i - 5) for k in range(5)] for i in range(10)]

    @staticmethod
    def hand_has_empty_homes(board,hand_idx):
        if (board[hand_idx[0][0]][hand_idx[0][1]] is None) or (board[hand_idx[1][0]][hand_idx[1][1]] is None)\
            or (board[hand_idx[2][0]][hand_idx[2][1]] is None) or (board[hand_idx[3][0]][hand_idx[3][1]] is None)\
                or (board[hand_idx[4][0]][hand_idx[4][1]] is None):
            return True
        else: return False

    @staticmethod
    def hand_category(board,hand_idx):
        _has_empty=False
        _flush=False
        _royal_straight=False
        _straight=False
        _four_of_a_kind=False
        _full_house=False
        _three_of_a_kind=False
        _two_pair=False
        _one_pair=False

        R = {"A": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "T": 0, "J": 0, "Q": 0, "K": 0}
        R_values_count=[0,0,0,0,0,0]
        S={"C":0, "D":0, "H":0, "S":0}

        values = [Card.rank_to_value[board[r][c].rank] for r, c in hand_idx if board[r][c] is not None]

        for r,c in hand_idx:
            if board[r][c] is not None:
              R[board[r][c].rank]+=1
              S[board[r][c].suite] += 1
            elif _has_empty==False:
                _has_empty=True

        for v in R.values():
            R_values_count[v]+=1

        if 5 in S.values(): _flush=True
        if R_values_count[4]==1: _four_of_a_kind=True
        if R_values_count[3]==1:
            if R_values_count[2]==1: _full_house=True
            else:_three_of_a_kind=True
        if R_values_count[2]==2:_two_pair=True
        elif R_values_count[2]==1:_one_pair=True

        if _has_empty == False:
            # region  royal straight check
            if ((board[hand_idx[0][0]][hand_idx[0][1]].rank == "T" and board[hand_idx[1][0]][hand_idx[1][1]].rank == "J" \
                 and board[hand_idx[2][0]][hand_idx[2][1]].rank == "Q" and board[hand_idx[3][0]][
                     hand_idx[3][1]].rank == "K" \
                 and board[hand_idx[4][0]][hand_idx[4][1]].rank == "A") \
                    or \
                    (board[hand_idx[0][0]][hand_idx[0][1]].rank == "A" and board[hand_idx[1][0]][
                        hand_idx[1][1]].rank == "K" \
                     and board[hand_idx[2][0]][hand_idx[2][1]].rank == "Q" and board[hand_idx[3][0]][
                         hand_idx[3][1]].rank == "J" \
                     and board[hand_idx[4][0]][hand_idx[4][1]].rank == "T")) \
                    :
                _royal_straight = True
            # endregion
            # region straight check
            if values[0] < values[1]:
                if values[0] + 1 == values[1] and values[1] + 1 == values[2] and values[2] + 1 == values[3] and \
                        values[3] + 1 == values[4]: _straight = True
            elif values[0] == values[1] + 1 and values[1] == values[2] + 1 and values[2] == values[3] + 1 and \
                    values[3] == values[4] + 1:
                _straight = True
            # endregion


        if _royal_straight and _flush:
            return Hand.Royal_Flush
        elif _straight and _flush:
            return Hand.Straight_Flush
        elif _straight or _royal_straight:
            return Hand.Straight
        elif _flush:
            return Hand.Flush
        elif _four_of_a_kind:
            return Hand.Four_Of_A_Kind
        elif _full_house:
            return Hand.Full_House
        elif _three_of_a_kind:
            return Hand.Three_Of_A_Kind
        elif _two_pair:
            return Hand.Two_Pair
        elif _one_pair:
            return Hand.One_Pair
        else:
            return Hand.High_Card

class PointSystem:
    def __init__(self,point_system_name='British',point_system={'Royal_Flush':30,'Straight_Flush':30,'Four_Of_A_Kind':16,'Full_House':10,
                                    'Flush':5,'Straight':12,'Three_Of_A_Kind':6,'Two_Pair':3,'One_Pair':1,'High_Card':0}):
        self.point_system=point_system
        self.point_system_name=point_system_name
    def get_board_score(self, board):
        total_points=0
        for i in range(10):
            total_points+=self.point_system[Hand.Hand_Id_to_Category_Map[Hand.hand_category(board, Hand.hands_idx[i])]]
        return total_points

class GameSimulator:
    @staticmethod
    def simulate(point_system_object,poker_square_player_class,verbose=False,timeout_second=2,predefined_score=-1,consider_instance_creation_time=True,random_state=None):
        remaining_time = timeout_second*1000
        start = time.time()
        poker_square_player_object=poker_square_player_class()
        end = time.time()
        execution_time_milliseconds = round((end - start) * 1000)
        if consider_instance_creation_time:
          remaining_time = remaining_time - execution_time_milliseconds
          if remaining_time < 0:
              return predefined_score

        cards=Deck.shuffle(Deck.get_all_cards(),random_state=random_state)
        board=[[None,None,None,None,None],
               [None,None,None,None,None],
               [None,None,None,None,None],
               [None,None,None,None,None],
               [None,None,None,None,None],]
        for move_num in range(25):
            card=cards[move_num]
            start = time.time()
            row,col=poker_square_player_object.move(card.__copy__(),remaining_time)
            end = time.time()
            execution_time_milliseconds=round((end - start) * 1000)
            remaining_time=remaining_time-execution_time_milliseconds
            if (row<0 or row>4 or col<0 or col>4) or board[row][col] is not None:
                return predefined_score
            if remaining_time<0:
                return predefined_score
            board[row][col]=card

            if verbose:
                Board.print_board(board)

        score=point_system_object.get_board_score(board)
        return score,remaining_time

if __name__ == '__main__':
  num_simulation=1
  parameters={'point_system_object':PointSystem(),
              'poker_square_player_class':PMCTSPlayer,
              'verbose':True,
              'timeout_second':10000,
              'predefined_score':-1,
              'consider_instance_creation_time':True,
              'random_state':None
              }
  # region exe
  random.seed(parameters['random_state'])
  simulation_score_results=[]
  simulation_rem_time_results=[]
  pool = multiprocessing.Pool(1)
  for i in range(num_simulation):
    res = pool.apply_async(GameSimulator.simulate, list(parameters.values()))
    try:
      score,rem_time=res.get(parameters['timeout_second'])
      print(f"score:{score}, rem time (ms):{rem_time}")
    except:
      score=parameters['predefined_score']
      rem_time=0
      print('timeout')
    simulation_score_results.append(score)
    simulation_rem_time_results.append(rem_time)
  # endregion
  print(f"\n{parameters['point_system_object'].point_system_name} score | avg{f' ± stdev'if len(simulation_score_results)>1 else ''}: {mean(simulation_score_results):.2f}{f' ± {stdev(simulation_score_results):.2f}'if len(simulation_score_results)>1 else ''} ,min score: {min(simulation_score_results)}, max score: {max(simulation_score_results)}")
