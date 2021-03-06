import random

#from player import Player
from player import ManualPlayer, MiniMaxPlayer, AlphaBetaPlayer
from board import Board
import time
import numpy as np
import matplotlib.pyplot as plt

class Game():
    """ Game class for performing game simulations.
    
    General rules of the game are defined in this class. For example:
    - if 4 pieces are connected by a player (in case k=4) horizontally, vertically, or
      diagonally, the player wins.
    - one of the m columns in the mxn grid of the board must be chosen as input. 

    """

    def __init__(self, player1, player2, size=(7,7), k=4):
        """ Initialises a game.
        
        Args:
            player1 (Player): First player
            player2 (Player): Second player
        """
        self.player1 = player1
        self.player2 = player2
        self.k = k
        self.size = size

        self.max_player, self.min_player = self.select_starting_player()
        self.board = None
        self.times_list = []
        self.states_visited_list = []

    def initialize_game(self):
        """Initialise board for game."""
        self.board = Board(size=self.size, k=self.k)
    
    def play(self, num_moves=None):
        """ Simulates an entire game. 
        
        Prints out the necessary information. 
        """
        print(f"{self.max_player} starts the game.")
        curr_player, waiter = self.max_player, self.min_player

        self.initialize_game() #initialize board for game 
            
        # Simulates the game, until a player has lost
        finished = False
        while not finished:
            self.drawboard()
            print(f"{curr_player}, your turn:")

            start = time.time()
            target_col = curr_player.select_target(self.board)
            target_cell = self.board.get_cell(target_col)
            time_taken = time.time() - start
            states_visited = curr_player.states_visited
            self.states_visited_list.append(states_visited)

            self.times_list.append(time_taken)

            self.board.make_move(target_cell)

            # Game over if either player has lost
            winner = self.board.winner_check()
            if winner > 0:
                finished = True
            else:
                curr_player, waiter = waiter, curr_player  
            

        # Show final results
        self.drawboard()
        print(f"{curr_player} has won!")

    def drawboard(self):
        """Draw board on terminal."""
        self.board.print()
        
    def select_starting_player(self):
        """ Selects a player to start at random (Max is always starting player)
        
        Returns: 
            max_player {Player()}: player that starts game.
            min_player {Player()}: opponent of max_player"""
        # Chooses the player to start first
        max_player = self.player1
        min_player = self.player2
        
        min_player.is_min = True
            
        return max_player, min_player
    
    def plot_states(self):
        plt.figure()
        plt.plot(np.arange(len(self.states_visited_list)), self.states_visited_list)
        plt.xlabel("Episodes")
        plt.ylabel("States Visited")
        plt.show()

if __name__ == '__main__':
    # SANDBOX for you to play and test your methods
    #player1 = MinMaxPlayer(name="Jaime", max_depth=4)
    #player2 = MinMaxPlayer(name="Mart", max_depth=3)

    #num_moves = 30 #number of moves to average results over (replications)

    player1 = AlphaBetaPlayer(name="Jaime", max_depth=5)
    #player1 = ManualPlayer(name="Jaime", max_depth=5)
    player2 = AlphaBetaPlayer(name="Mart", max_depth=5)
    test = Game(player1,player2,size=(7,6), k=4)

    test.play(num_moves=None)

     