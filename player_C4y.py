import random
from board_C4 import Board
from convert import CellConverter
import numpy as np

class Player():
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name

    def __str__(self):
        return self.name
    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError

class MinMaxPlayer(Player):
    def __init__(self, max_depth=5, name=None):
        super().__init__(name)

        self.max_depth = max_depth
        self.is_min = None

    def _get_diagonals(self,board,row,col):
        """Retrieves positive and negative diagonals from a cell in a grid.
        
        Args:
            board {Board()}: current board state.
            row {int}: row of cell to evaluate
            col {int}: column of cell to evaluate
        
        Returns:
            Positive and negative diagonal arrays that cross at the cell (row,col).
        
        """
        pos_diag1 = np.fliplr(np.flipud(board.state[:row+1,:col+1])).diagonal()[::-1]
        pos_diag2 = board.state[-(board.height-row):,-(board.width-col):].diagonal()[1:]

        pos_diag = np.concatenate((pos_diag1, pos_diag2))

        neg_diag1 = np.flipud(board.state[:row+1, col:]).diagonal()
        neg_diag2 = np.fliplr(board.state[-(board.height-row):,:-(board.width-col-1)]).diagonal()[1:][::-1]

        neg_diag = np.concatenate((neg_diag2, neg_diag1))

        diags = [pos_diag, neg_diag]

        return diags
    
    def heuristic(self, board):
        """Calculates the heuristic value of a specific state for the current player (Min or Max)."""
        value = 0
        state = board.state

        #calculate heuristic by considering each players' current streaks
        # ---> heuristic is calculated as +-10^{streak-1}, where the + corresponds to Max() and - to Min()
        for col in range(self.width):
            for row in range(self.height):
                #check horizontal streaks
                board_row = state[row,:]
                streak = board.streak_check(board_row, get_streak=True)
                if not self.is_min:    
                    value += 10**(streak-1)
                else:
                    value -= 10**(streak-1)

                #check vertical streaks
                board_col = state[:,col]
                streak = board.streak_check(board_col, get_streak=True)
                if not self.is_min:    
                    value += 10**(streak-1)
                else:
                    value -= 10**(streak-1)

                #check diagonal streaks
                diags = self._get_diagonals(board,row,col)
                for board_diag in diags:
                    streak = self.streak_check(board_diag, get_streak=True)
                    if not self.is_min:    
                        value += 10**(streak-1)
                    else:
                        value -= 10**(streak-1)

        return value

    def should_replace_move(self, value):
        """Function to determine if move shold be replaced by current node being evaluated."""
        if self.is_min:
            return value < self.best_value
        else:
            return value > self.best_value
    
    def max(self, depth, board):
        if board.is_full:
            print("Board is full")
            return -float("inf"), -1
        elif depth == 0:
            print("Depth is 0")
            return self.heuristic(board), -1

        #initialise best value to be infinite and negative such that any action will be chosen at first
        self.best_value = -float("inf")

        best_move = -1

        #iterate over all possible actions and retrieve best score and thus move
        children = board._children
        for child in children:
            childboard, move = child
            print(childboard)
            temp = self.min(childboard, depth-1)[0]
            if self.should_replace_move(temp):
                self.best_value = temp
                best_move = move

        return self.best_value, best_move

    def min(self, depth, board):
        if board.is_full:
            print("Board is full")
            return float("inf"), -1
        elif depth == 0:
            print("Depth is 0")
            return self.heuristic(board), -1

        #initialise best value to be infinite and positive such that any action will be chosen at first
        self.best_value = float("inf")

        best_move = -1

        #iterate over all possible actions and retrieve best score and thus move
        children = board._children
        for child in children:
            childboard, move = child
            print(childboard)
            temp = self.max(childboard, depth-1)[0]
            if self.should_replace_move(temp):
                self.best_value = temp
                best_move = move
                print(self.best_value, best_move)

        return self.best_value, best_move

    def select_target(self, board):
        if not self.is_min:
            best_value, best_move = self.max(self.max_depth, board)
        else:
            best_value, best_move = self.min(self.max_depth, board)

        return best_move

class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(name)

    def select_target(self, board):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        while True:
            try:
                target_col = int(input("Enter the target column value: "))
                return target_col
            except ValueError as error:
                print(error)

class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        super().__init__(name)

    def select_target(self, board):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        column = random.randint(1, board.width)

        return column

if __name__ == '__main__':
    player = MinMaxPlayer()
    board = Board()
    print(player.select_target(board))
