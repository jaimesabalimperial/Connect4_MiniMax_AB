import random

#from player import Player
from convert import CellConverter
from board_C4 import Board

class Game:
    """ Game class for performing game simulations.
    
    General rules of the game are defined in this class. For example:
    - if a ship is hit, the attacker has the right to play another time.
    - if all the opponent's ships have been sunk, the game stops, and the results are printed
    """

    def __init__(self, player1, player2, size = (7,7), k = 4 ):
        """ Initialises a game.
        
        Args:
            player1 (Player): First player
            player2 (Player): Second player
        """
        self.player1 = player1
        self.player2 = player2
        
        self.board = Board(size, k)
    
    def play(self):
        """ Simulates an entire game. 
        
        Prints out the necessary information (boards without ships, positions under attack...)
        """
        board = self.board
        player_current, waiter = self.select_starting_player()
        print(f"{player_current} starts the game.")
            
        # Simulates the game, until a player has lost
        while board.winner_check() < 1 :
            board.print()
            print(f"{player_current}, your turn:")

            target_col = player_current.select_target(board)
            target_cell = board.get_cell(target_col)
            if player_current is self.player1:
                board.add_move_to_board(1,target_cell)
            else:
                board.add_move_to_board(2,target_cell)

                # Game over if either player has lost
            
            winner = board.winner_check()
            if winner > 0:
                break
            # Players swap roles
            player_current, waiter = waiter, player_current  

        # Show final results
        board.print()
        print(f"{player_current} has won!")
        
    def select_starting_player(self):
        """ Selects a player to start at random. """
        # Chooses the player to start first
        if random.choice([True, False]):
            attacker = self.player1
            opponent = self.player2
        else:
            attacker = self.player2
            opponent = self.player1
            
        return attacker, opponent

if __name__ == '__main__':
    # SANDBOX for you to play and test your methods
    test = Game("Toomas", "Peeter")
    test.play()
    
    # Automatic board
    
     