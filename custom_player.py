from poker_squares_utils import *
from node import Node
from montecarlo import MonteCarlo

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
    def __init__(self,point_sys=PointSystem(),n_sim=25):
        self.name = 'PMCTSPlayer'
        self.board=Board.create_random_board(25)
        self.point_sys=point_sys
        self.n_sim=n_sim
    def move(self,card,remaining_time):
        env = MonteCarlo(Node([self.board,card,self.point_sys]))#state: board, card:None, point_sys
        env.child_finder = PMCTSPlayer.child_finder
        env.node_evaluator = PMCTSPlayer.node_evaluator
        env.simulate(self.n_sim)
        chosen_child_node = env.make_choice()
        for r in range(5):
            for c in range(5):
                if (self.board[r][c] is None) and (chosen_child_node.state[0][r][c] is not None):
                    self.board = chosen_child_node.state[0]
                    return r,c
    @staticmethod
    def child_finder(node, montecarlo):
        board = node.state[0]
        card = node.state[1]
        seen_cards = set([item for r in board for item in r if item is not None])
        if card is None:
            unseen_cards = set(Deck.get_all_cards()).difference(seen_cards)
        else:
            unseen_cards = set([card])
        for i in range(5):
            for j in range(5):
                if board[i][j] is None:
                    for c in unseen_cards:
                        cloned_board = Board.clone_board(board)
                        cloned_board[i][j] = c
                        child = Node([cloned_board, None,node.state[2]])
                        node.add_child(child)

    @staticmethod
    def node_evaluator(node, montecarlo):
        return node.state[2].get_board_score(node.state[0])










