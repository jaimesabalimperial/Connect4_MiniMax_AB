import random

#from player import Player
from convert import CellConverter
from player_C4y import ManualPlayer, MiniMaxPlayer, AlphaBetaPlayer
from board_C4 import Board
import time
import numpy as np
import matplotlib.pyplot as plt

class Game():
    """ Game class for performing game simulations.
    
    General rules of the game are defined in this class. For example:
    - if a ship is hit, the attacker has the right to play another time.
    - if all the opponent's ships have been sunk, the game stops, and the results are printed
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
        self.board = Board(size=self.size, k=self.k)
        self.times_list = []
        self.states_visited_list = []
    
    def play(self):
        """ Simulates an entire game. 
        
        Prints out the necessary information (boards without ships, positions under attack...)
        """
        print(f"{self.max_player} starts the game.")
        curr_player, waiter = self.max_player, self.min_player

            
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
                # Players swap roles
                curr_player, waiter = waiter, curr_player  

        # Show final results
        self.drawboard()
        print(f"{curr_player} has won!")

    def drawboard(self):
        self.board.print()
        
    def select_starting_player(self):
        """ Selects a player to start at random (Max is always starting player)"""
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
    player1 = AlphaBetaPlayer(name="Jaime", max_depth=5)
    #player1 = ManualPlayer(name="Jaime", max_depth=5)
    player2 = AlphaBetaPlayer(name="Mart", max_depth=5)
    test = Game(player1,player2,size=(7,6), k=4)
    test.play()

    #test.plot_states()
    #test.plot_time()

    print("Average time taken to compute results = ", np.mean(test.times_list))
    # Automatic board
    
     