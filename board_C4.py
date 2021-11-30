import sys
from copy import deepcopy
#sys.path.append("C:\\Users\\jsaimesabal\\Desktop\\ICL\\Intro to Symbolic AI\\CW2\\python_cw3_mb1221\\battleship")
import numpy as np

class Board():
    """ Class representing the board of the player. 
            
    Acts as an interface between the player and its ships.
    """
    def __init__(self, size=(7,7), k=4):
        """ Initialises a Board given a list of ships. 
        
        Args:
            size (tuple[int, int]): (width, height) of the board (in terms of 
                number of cells). Defaults to (10, 10).
            k (int): The number of connected positions (horizontally, diagonally, or vertically)
                needed to win a game.
                
        Raises:
            ValueError if the number of ships is False
        """
        self.width = size[0]
        self.height = size[1]
        
        # Set of cells that have been checked for each player
        # Used for visualising the board
        self.state = np.zeros((self.width, self.height))
        self.max_player_cells = []
        self.min_player_cells = []
        self.k = k
        self.recur_moves = 0
        self.game_moves = 0

    def make_move(self, cell, recursion=False):
        x,y = cell
        if not recursion:
            player = self.game_moves % 2 + 1
            self.game_moves += 1
        else:
            player = self.recur_moves % 2 + 1
            self.recur_moves +=1

        self.state[y][x] = player
        
        if player == 1:
            self.max_player_cells.append(cell)
        else:
            self.min_player_cells.append(cell)


    def get_children(self):
        children = []
        for col in range(1,self.width+1):
            if 0 in self.state[:,col-1]:
                child_node = deepcopy(self)
                move_cell = child_node.get_cell(col)
                child_node.make_move(move_cell, recursion=True)
                children.append((child_node, move_cell))

        return children

    def is_full(self):
        """Returns true if the board is full (case terminal node where the game 
        ends with a draw)."""
        return self.game_moves == int(self.width*self.height)
        
    def winner_check(self):
        """ Check whether someone has won the game.
        
        Returns:
            bool : return True if all ships on the board have sunk.
               return False otherwise.
        """
        #Column check
        board = self.state
        for col in range(self.width):
            board_col = board[:,col]
            winner = self.streak_check(board_col)
            if winner > 0:
                return winner
        #Row check
        for row in range(self.height):
            board_row = board[row,:]
            winner = self.streak_check(board_row)
            if winner > 0:
                return winner

        diags = [board[::-1,:].diagonal(i) for i in range(-3,4)]
        diags.extend(board.diagonal(i) for i in range(3,-4,-1))
        all_diags = [n.tolist() for n in diags if len(n) >= self.k]
        for diag in all_diags:
            winner = self.streak_check(diag)
            if winner > 0:
                return winner
        return 0

    def streak_check_heuristic(self, input):
        player = 0
        val_to_player = {1:"Max", 2:"Min"}
        streaks_dict = {"Max":[], "Min":[]}

        for cell in input:
            if cell == 0:
                continue

            if val_to_player[cell] == player:
                streaks_dict[player][-1] += 1
            else: 
                player = val_to_player[cell]
                streaks_dict[player].append(1)

            if streaks_dict[player][-1] == self.k:
                return streaks_dict

        return streaks_dict


    def streak_check(self, input):
        player = 0
        streak = 0
        for cell in input:
            if cell == player:
                streak += 1
            else: 
                player = cell
                streak = 1
            if streak == self.k and player > 0:
                return player
        return 0


    def get_cell(self, column_nr):
        column = self.state[:,column_nr-1]
        if 1 in column or 2 in column:
            y_coord = np.where(column)[0].max() + 1
            cell = (column_nr-1, y_coord)
            return cell
        else: 
            return (column_nr-1, 0)
  
    def print(self):
        """ Visualise the board on the terminal.
        
        Args:
            show_ships (bool): Shows the ships on the board. Defaults to False. 
            
        Returns:
            None
        """
        array_board = self._build_array()
        board_str = self._array_to_str(array_board)
        print(board_str)

    def _build_array(self):
        """ Generate an array representation of the Board for visualisation."""
        array_board = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        for cells in self.max_player_cells:
            x_1, y_1 = cells
            array_board[self.height - (y_1+1)][x_1] = 'X'

        for cells in self.min_player_cells:
            x_2, y_2 = cells
            array_board[self.height - (y_2+1)][x_2] = '0'

        return array_board
    
    def _array_to_str(self, array_board):
        """ Convert an array representation of the Board to string 
            representation to facilitate visualisation.
        """
        list_lines = []

        array_first_line = [str(code) for code in range(1, self.width + 1)]
        first_line = ' ' * 6 + (' ' * 5).join(array_first_line) + ' \n'

        for index_line, array_line in enumerate(array_board, 1):
            number_spaces_before_line = 2 - len(str(index_line))
            space_before_line = number_spaces_before_line * ' '
            list_lines.append(f'{space_before_line}{self.height - index_line + 1} |  ' + '  |  '.join(array_line) + '  |\n')

        line_dashes = '   ' + '-' * 6 * self.width + '-\n'

        board_str = first_line + line_dashes + line_dashes.join(list_lines) + line_dashes

        return board_str


if __name__ == '__main__':
    # SANDBOX for you to play and test your methods

    
    # Automatic board
    board = Board()
    col = 1  
    move = board.get_cell(col)
    board.make_move(move)
    print(board._children)

