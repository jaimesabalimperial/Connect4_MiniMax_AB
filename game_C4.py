import random

#from player import Player
from convert import CellConverter
from player_C4y import ManualPlayer
from board_C4 import Board

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

        self.max_player, self.min_player = self.select_starting_player()
        
        self.board = Board(size, k)
    
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

            target_col = curr_player.select_target(self.board)
            target_cell = self.board.get_cell(target_col)

            self.board.add_move_to_board(target_cell)

            # Game over if either player has lost
            winner = self.board.winner_check()
            if winner > 0:
                finished = True
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
        if random.choice([True, False]):
            max_player = self.player1
            min_player = self.player2
        else:
            max_player = self.player2
            min_player = self.player1
        
        min_player.is_min = True
            
        return max_player, min_player

if __name__ == '__main__':
    # SANDBOX for you to play and test your methods
    player1 = ManualPlayer(name="Jaime")
    player2 = ManualPlayer(name="Mart")
    test = Game(player1, player2)
    test.play()
    
    # Automatic board
    
     