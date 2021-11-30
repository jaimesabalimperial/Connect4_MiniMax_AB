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

    def get_value(self, board, line):
        value = 0
        streaks_dict = board.streak_check_heuristic(line)
        for player, streaks in streaks_dict.items(): 
            for streak in streaks:
                if player == "Max":
                    value += 10**(streak-1)
                elif player == "Min":
                    value -= 10**(streak-1)

        return value
    
    def heuristic(self, board):
        """Calculates the heuristic value of a specific state for the current player (Min or Max)."""
        value = 0
        state = board.state
        #calculate heuristic by considering each players' current streaks
        # ---> heuristic is calculated as +-10^{streak-1}, where the + corresponds to Max() and - to Min()
        for row in range(board.height):
            #check horizontal streaks
            board_row = state[row,:]
            value += self.get_value(board, board_row)

        for col in range(board.width):
            #check vertical streaks
            board_col = state[:,col]
            value += self.get_value(board, board_col)

        for col in range(board.width):
            for row in range(board.height):
                #check diagonal streaks
                diags = self._get_diagonals(board,row,col)
                for board_diag in diags:
                    value += self.get_value(board, board_diag)

        return value

    def should_replace_move(self, value, best_value):
        """Function to determine if move shold be replaced by current node being evaluated."""
        if self.is_min:
            return value < best_value
        else:
            return value > best_value
    
    def max(self, board, player, depth=0):
        if board.is_full():
            return -float("inf") if not self.is_min else float("inf"), -1
        elif depth == self.max_depth:
            return self.heuristic(board), None
        elif board.game_moves == 0:
            return self.heuristic(board), board.width // 2 + 1
        

        #initialise best value to be infinite and negative such that any action will be chosen at first
        if player:
            best_value = -float("inf")  
        else:
            best_value = float("inf")  
        
        best_move = None

        #iterate over all possible actions and retrieve best score and thus move
        children = board.get_children()
        for child in children:
            child_state, move_cell = child
            child_val = self.min(child_state, not player, depth+1)[0]

            if self.should_replace_move(child_val, best_value):
                best_value = child_val
                best_move = move_cell[0]

        print(best_value, best_move)

        return best_value, best_move

    def min(self, board, player, depth=0):
        if board.is_full():
            return float("inf") if self.is_min else -float("inf"), -1
        elif depth == self.max_depth:
            return self.heuristic(board), None

        #initialise best value to be infinite and positive such that any action will be chosen at first
        if player:
            best_value = float("inf")
        else:
            best_value = -float("inf")  

        best_move = None

        #iterate over all possible actions and retrieve best score and thus move
        children = board.get_children()
        for child in children:
            child_state, move_cell = child
            child_val = self.max(child_state, not player, depth+1)[0]

            if self.should_replace_move(child_val, best_value):
                best_value = child_val
                best_move = move_cell[0]
        
        print(best_value, best_move)

        return best_value, best_move

    def select_target(self, board):
        if not self.is_min:
            best_value, best_move = self.max(board, self.is_min)
        else:
            best_value, best_move = self.min(board, self.is_min)

        print(best_move)
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
    board.make_move(board.get_cell(1))
    board.make_move(board.get_cell(2))
    board.make_move(board.get_cell(1))
    board.make_move(board.get_cell(2))
    board.make_move(board.get_cell(1))
    print(board.state[1])
    print(board.streak_check_heuristic(board.state[1]))
    #print(player.heuristic(board))
    #print(player._get_diagonals(board, 1, 0))
